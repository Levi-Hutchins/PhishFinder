from pydantic import BaseModel
from typing import Dict, Optional

class Email(BaseModel):
    subject: str
    title: Optional[str] = None
    body: str

class PhishingLink(BaseModel):
    url_link: str

class URLScanResponse(BaseModel):
    id: str

class PredictionResponse(BaseModel):
    status: str

class EngineResults(BaseModel):
    category: str
    result: str
    method: str
    engine_name: str

class Stats(BaseModel):
    harmless: int
    malicious: int
    suspicious: int
    undetected: int
    timeout: int

class ScanAnalysisReport(BaseModel):
    stats: Stats
    results: Dict[str, EngineResults]
