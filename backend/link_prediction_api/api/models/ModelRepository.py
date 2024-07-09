from pydantic import BaseModel
from typing import Optional

class PredictionResult(BaseModel):
    link_status: str

class URL_Link(BaseModel):
    link: str

class Email(BaseModel):
    subject: str
    title: Optional[str] = None
    body: str