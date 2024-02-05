from pydantic import BaseModel

class PredictionResponse(BaseModel):
    status: str