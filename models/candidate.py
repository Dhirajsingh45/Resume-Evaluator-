from pydantic import BaseModel


class Candidate(BaseModel):
    name: str
    email: str|None
    phone: str|None
    location: str
    education: list[str]
    skills: list[str]
    experience: list[str]
    projects: list[str]
    certifications: list[str]