from pydantic import BaseModel


class EngineResults(BaseModel):
    category: str
    result: str
    method: str
    engine_name: str