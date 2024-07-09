
from logger_config import logger
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware


from models.ModelRepository import URL_Link, PredictionResult
from utils import url_processing, model_prediction

from service.cloudflare_service import url_cloudflare_submission


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
    #logger.info(f"{request.client.host} {request.method} /get_health_status")
    logger.task("test")
    return{"message":"All systems go"}






@app.post("/link_prediction")
async def link_model_prediction(user_req: URL_Link, request: Request, background_tasks: BackgroundTasks):

    logger.info(f"{request.client.host} {request.method} /link_prediction")

    background_tasks.add_task(url_cloudflare_submission, user_req)


    x_labels = url_processing.get_features(user_req.link)
    if x_labels == 404:
        logger.warning(f"Url Processing Status 404: Investigate Link: {user_req.link}")
        return "suspicious"
    
    if len(x_labels) != 9:
        logger.error(f"URL Processing did not source 9 labels, link: {user_req.link}")
        raise HTTPException(status_code=500, detail="Issue with url processing")

    prediction = model_prediction.make_prediction(x_labels)

    if prediction == 500:
        logger.error(f"Error making prediction {user_req.link} {x_labels}")

    if prediction[0] == -1: 
        return PredictionResult(status="phishing")
    elif prediction[0] == 0: 
        return PredictionResult(status="suspicious")
    else: 
        return PredictionResult(status="legitimate")


    

