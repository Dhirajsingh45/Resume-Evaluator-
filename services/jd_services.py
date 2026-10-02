import os
import json

from dotenv import load_dotenv
from groq import Groq

from models.job import Job


load_dotenv()

api_key = os.getenv("Groq_api_key")

if not api_key:
    raise ValueError("Groq API key not found")

client = Groq(api_key=api_key)


def make_strict_schema(schema):

    if isinstance(schema, dict):

        if schema.get("type") == "object":
            schema["additionalProperties"] = False

        for value in schema.values():
            make_strict_schema(value)

    elif isinstance(schema, list):

        for item in schema:
            make_strict_schema(item)

    return schema


def extract_job_description(jd_text: str):

    schema = Job.model_json_schema()

    schema = make_strict_schema(schema)

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": """
You are a job description analysis system.

Extract structured job requirements from the given job description.

Rules:

1. Extract the job title.
2. Extract required experience if mentioned.
3. Extract important technical skills and requirements.
4. Classify each requirement as either:
   - required
   - preferred
5. Assign weights to requirements.
6. Required skills should generally receive higher weights than preferred skills.
7. The total of all requirement weights must equal 100.
8. Only use information present in the job description.
9. Do not invent requirements.
"""
            },
            {
                "role": "user",
                "content": jd_text
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "job",
                "strict": True,
                "schema": schema
            }
        }
    )

    raw_json = response.choices[0].message.content

    data = json.loads(raw_json)

    job = Job.model_validate(data)

    return job