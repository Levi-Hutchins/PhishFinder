from pydantic import BaseModel

class PhishingLink(BaseModel):
    url_link: str