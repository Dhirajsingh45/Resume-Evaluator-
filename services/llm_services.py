import os
import json
from dotenv import load_dotenv
from groq import Groq

from models.candidate import Candidate

load_dotenv()

api_key = os.getenv("Groq_api_key")

if not api_key:
    raise ValueError("Groq API key not found")

client = Groq(api_key=api_key)


def make_strict_schema(schema):
    """
    Make every object in a JSON schema
    compatible with Groq strict structured output.
    """

    if isinstance(schema, dict):

        # Every object must have additionalProperties = False
        if schema.get("type") == "object":
            schema["additionalProperties"] = False

        # Recursively process nested schemas
        for value in schema.values():
            make_strict_schema(value)

    elif isinstance(schema, list):

        for item in schema:
            make_strict_schema(item)

    return schema


def extract_candidate(resume_text: str):

    schema = Candidate.model_json_schema()

    # Make schema Groq strict-compatible
    schema = make_strict_schema(schema)

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": """
You are a resume information extraction system.

Extract candidate information from the resume.

Rules:
- Only use information present in the resume.
- Do not invent information.
- If a field is not present, return null for nullable fields.
- Return skills, education, experience, projects and certifications as lists.
"""
            },
            {
                "role": "user",
                "content": resume_text
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "candidate",
                "strict": True,
                "schema": schema
            }
        }
    )

    raw_json = response.choices[0].message.content

    data = json.loads(raw_json)

    candidate = Candidate.model_validate(data)

    return candidate