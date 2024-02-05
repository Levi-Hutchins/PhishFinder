from pydantic import BaseModel

from typing import Dict, Optional

class Email(BaseModel):
    subject: str
    title: Optional[str] = None
    body: str
