from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.API_KEYS import VIRUS_TOTAL
from pysafebrowsing import SafeBrowsing
from fastapi.responses import JSONResponse
from models import URLScanResponse, ScanAnalysisReport
import models
import requests
from fastapi import Request

from scripts import url_processing, model_prediction
from pprint import pprint


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/link_prediction/")
async def inhouse_model_prediction(user_req: models.PhishingLink):
    x_labels = url_processing.get_url_prediction_values(user_req.url_link)
    prediction = model_prediction.make_prediction(x_labels)
    if prediction[0] == -1: return JSONResponse("phishing")
    elif prediction[0] == 0: return JSONResponse("suspicious")
    else: return JSONResponse("legitimate")


@app.post("/virus_total_urlscan/")
async def virus_total_api(user_req: Request):
    scan_url = await user_req.json()
    url = "https://www.virustotal.com/api/v3/urls"
    payload = { "url": scan_url["url_link"] }
    headers = {
        "accept": "application/json",
        "x-apikey": f"{VIRUS_TOTAL}",
        "content-type": "application/x-www-form-urlencoded"
    }

    user_requested_url = URLScanResponse(requests.post(url, data=payload, headers=headers).json()["data"])
    test = await virus_total_analysis(user_requested_url)
    return JSONResponse(content=test.to_dict())




async def virus_total_analysis(scanned_url: URLScanResponse):
    url = f"https://www.virustotal.com/api/v3/analyses/{scanned_url.id}"

    headers = {
        "accept": "application/json",
        "x-apikey": f"{VIRUS_TOTAL}"
    }

    analysis_response = requests.get(url, headers=headers).json()
    stats_data = analysis_response['data']['attributes']['stats']
    engine_results = analysis_response['data']['attributes']['results']
    analysis_report = ScanAnalysisReport(stats_data, engine_results)
    return analysis_report






