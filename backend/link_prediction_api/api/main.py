
import logging
from logFormat import CustomFormatter
from mangum import Mangum

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from mangum import Mangum

from models.PhishingLink import PhishingLink
from models.PredictionResponse import PredictionResponse


from scripts import url_processing, model_prediction
import sys

sys.dont_write_bytecode = True

#Logging Config 
logger = logging.getLogger("PhishingLinkAPI")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()

ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.propagate = False
logger.addHandler(ch)



app = FastAPI()
handler = Mangum(app)
logger.info("phishing_link_api spinning up...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health_status")
async def get_health_status():
    logger.info("Request Made - [GET] /get_health_status")
    return{"Status Code":200,"message":"All systems go"}


@app.post("/link_prediction/")
async def inhouse_model_prediction(user_req: PhishingLink):
    logger.info("Request Made - [POST] /link_prediction")

    x_labels = url_processing.get_features(user_req.url_link)

    if x_labels == 404:
        logger.warning(f"Url Processing Status 404: Investigate Link: {user_req.url_link}")
        return "phishing"
    # Some exception handling just incase url processing fails
    if len(x_labels) != 9:
        logger.error(f"URL Processing did not source 9 label, link: {user_req.url_link}")
        raise HTTPException(status_code=404, detail="Issue with url processing")
    
    prediction = model_prediction.make_prediction(x_labels)

    if prediction[0] == -1: 
        return PredictionResponse(status="phishing")
    elif prediction[0] == 0: 
        return PredictionResponse(status="suspicious")
    else: 
        return PredictionResponse(status="legitimate")


    

handler = Mangum(app=app)