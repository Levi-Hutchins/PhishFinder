from pydantic import BaseModel
from typing import Optional

class PredictionResult(BaseModel):
    status: str

class URL_Link(BaseModel):
    link: str

class Email(BaseModel):
    subject: str
    title: Optional[str] = None
    body: str