from pydantic import BaseModel
from typing import Dict
from .Stats import Stats
from .EngineResults import EngineResults

class ScanAnalysisReport(BaseModel):
    stats: Stats
    results: Dict[str, EngineResults]
