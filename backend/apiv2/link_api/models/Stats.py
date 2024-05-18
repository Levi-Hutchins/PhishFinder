from pydantic import BaseModel

class Stats(BaseModel):
    harmless: int
    malicious: int
    suspicious: int
    undetected: int
    timeout: int