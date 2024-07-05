
import logging
import os
import requests
from logFormat import CustomFormatter
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware


from models.PhishingLink import PhishingLink
from models.PredictionResponse import PredictionResponse


from scripts import url_processing, model_prediction
import sys

sys.dont_write_bytecode = True
load_dotenv()
#Logging Config 
logger = logging.getLogger("Link-ML-Service")
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()

ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
logger.propagate = False
logger.addHandler(ch)



app = FastAPI()

logger.info("Link-ML-Service Spinning Up...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health_status")
async def get_health_status(request: Request):
    logger.info(f"{request.client.host} {request.method} /get_health_status")
    return{"message":"All systems go"}


def url_cloudflare_submission(req:PhishingLink):

    headers = {
    "Content-Type": "application/json",
    "Authorization": os.getenv(CLOUDFLARE_APIKEY)
    }
    payload = {"url": req.url_link}

    response = requests.post(os.getenv(CLOUDFLARE_URLSCAN_ENDPOINT), headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Request successful!")
        print(response.json())
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)




@app.post("/link_prediction")
async def link_model_prediction(user_req: PhishingLink, request: Request):
    logger.info(f"{request.client.host} {request.method} /link_prediction")

    x_labels = url_processing.get_features(user_req.url_link)
    if x_labels == 404:
        logger.warning(f"Url Processing Status 404: Investigate Link: {user_req.url_link}")
        return "suspicious"
    
    # Some exception handling just incase url processing fails
    if len(x_labels) != 9:
        logger.error(f"URL Processing did not source 9 labels, link: {user_req.url_link}")
        raise HTTPException(status_code=500, detail="Issue with url processing")

    prediction = model_prediction.make_prediction(x_labels)

    if prediction == 500:
        logger.error(f"Error making prediction {user_req.url_link} {x_labels}")

    if prediction[0] == -1: 
        return PredictionResponse(status="phishing")
    elif prediction[0] == 0: 
        return PredictionResponse(status="suspicious")
    else: 
        return PredictionResponse(status="legitimate")


    

