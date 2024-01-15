from fastapi import FastAPI
from fastapi.responses import JSONResponse

import models
from scripts import url_processing, model_prediction

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/link_prediction/")
async def create_item(link: models.PhishingLink):
    x_labels = url_processing.get_url_prediction_values(link.url_link)
    prediction = model_prediction.make_prediction(x_labels)
    return JSONResponse(int(prediction[0]))
