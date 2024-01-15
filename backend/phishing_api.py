from fastapi import FastAPI
from pysafebrowsing import SafeBrowsing
from fastapi.responses import JSONResponse

import models
from scripts import url_processing, model_prediction

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/link_prediction/")
async def inhouse_model_prediction(link: models.PhishingLink):
    x_labels = url_processing.get_url_prediction_values(link.url_link)
    prediction = model_prediction.make_prediction(x_labels)
    if prediction[0] == -1: return JSONResponse("phishing")
    elif prediction[0] == 0: return JSONResponse("suspicious")
    else: return JSONResponse("legitimate")

@app.post("/virus_total_analysis/")
async def virus_total_api():
    print()






