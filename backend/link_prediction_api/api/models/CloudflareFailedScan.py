from typing import List, Optional
from pydantic import BaseModel

class Error(BaseModel):
    name: str
    message: str
    detail: Optional[str]
    code: int

class ExtraOptions(BaseModel):
    screenshotsResolutions: List[str]

class Task(BaseModel):
    uuid: str
    url: str
    effectiveUrl: str
    status: str
    time: str
    visibility: str
    clientLocation: str
    clientType: str
    extraOptions: ExtraOptions
    scannedFrom: dict
    timeEnd: str
    errors: List[Error]
    success: bool
    serverASN: Optional[str]
    serverLocation: Optional[str]

class ScanResult(BaseModel):
    scan: Task

class Message(BaseModel):
    message: str

class FailedScan(BaseModel):
    success: bool
    messages: List[Message]
    result: ScanResult