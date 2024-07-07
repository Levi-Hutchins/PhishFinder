from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    message: str

class Result(BaseModel):
    visibility: str
    uuid: str
    url: str
    time: datetime

class CloudflareScanSubmission(BaseModel):
    success: bool
    messages: List[Message]
    result: Optional[Result] = None
    errors: List[str]