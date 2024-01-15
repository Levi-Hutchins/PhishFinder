from pydantic import BaseModel

class Email(BaseModel):
    subject: str
    title: str = None
    body: float
    #links: list(str)
    
class PhishingLink(BaseModel):
   url_link: str