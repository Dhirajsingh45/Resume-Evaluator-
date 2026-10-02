from pydantic import BaseModel


class Requirement(BaseModel):
    skill: str
    importance: str
    weight: int


class Job(BaseModel):
    job_title: str
    experience_required: str | None
    requirements: list[Requirement]