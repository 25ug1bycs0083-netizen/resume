from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=30, max_length=100_000)
    role: str = Field(min_length=2, max_length=100)
    filename: str | None = None


class JobMatchRequest(BaseModel):
    text: str = Field(min_length=30, max_length=100_000)
    role: str
