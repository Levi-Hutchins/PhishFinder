import httpx
import logging as logger

from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.EngineResults import EngineResults
from models.PhishingLink import PhishingLink
from models.URLScanResponse import URLScanResponse
from models.PredictionResponse import PredictionResponse
from models.ScanAnalysisReport import ScanAnalysisReport
from models.Stats import Stats

from scripts.config.API_KEYS import VIRUS_TOTAL

from scripts import url_processing, model_prediction
from scripts.url_processing import is_valid_url, clean_url


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_scanning_headers(user_req: str):
    url = "https://www.virustotal.com/api/v3/urls"
    payload = {"url": user_req}
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL
    }
    return url, payload, headers

def get_analytics_headers(scanned_url: URLScanResponse):
    url = f"https://www.virustotal.com/api/v3/analyses/{scanned_url.id}"
    headers = {
    "accept": "application/json",
    "x-apikey": VIRUS_TOTAL
    }
    return url, headers

@app.post("/link_prediction/")
async def inhouse_model_prediction(user_req: PhishingLink):
    x_labels = url_processing.get_features(user_req.url_link)

    if x_labels == 404:
        return "phishing"
    # Some exception handling just incase url processing fails
    if len(x_labels) != 9:
        raise HTTPException(status_code=404, detail="Issue with url processing")
    
    prediction = model_prediction.make_prediction(x_labels)

    if prediction[0] == -1: 
        return PredictionResponse(status="phishing")
    elif prediction[0] == 0: 
        return PredictionResponse(status="suspicious")
    else: 
        return PredictionResponse(status="legitimate")

@app.post("/virus_total_urlscan/")
async def virus_total_api(user_req: PhishingLink):

    unvalidated_url = clean_url(user_req.url_link)
    if is_valid_url(unvalidated_url):
    
    
        url, payload, headers = get_scanning_headers(unvalidated_url) # Is no validated
        url = clean_url(url)
        
        # url is now cleaned and validated - variable stays same to prevent recall of function
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=payload, headers=headers) # Issue here
                response.raise_for_status()

                try:
                    user_requested_url = URLScanResponse(id=response.json()["data"]["id"])
                except KeyError: 
                    
                    logger.error(f"KeyError: /virus_total_urlscan/: Request URL = {user_requested_url}")
                    # Logging
                    raise HTTPException(status_code=500, detail="Unexpected response format from VirusTotal API")

                analysis_report: ScanAnalysisReport = await virus_total_analysis(user_requested_url)
            return analysis_report.model_dump()
        except httpx.HTTPStatusError as exc:
            # Logging
            logger.error(f"HTTPStatusError: /virus_total_urlscan/  {exc}")
            raise HTTPException(status_code=exc.response.status_code, detail="Error from VirusTotal API")
        
        except httpx.RequestError as exc:
            # Logging
            logger.error(f"RequestError: /virus_total_urlscan/  {exc}")
            raise HTTPException(status_code=500, detail=f"HTTP request failed: {exc}")
    else:
        return 404


async def virus_total_analysis(scanned_url: URLScanResponse):
    
    
    url, headers = get_analytics_headers(scanned_url)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            try:
                analysis_response = response.json()
                stats_data = Stats(**analysis_response['data']['attributes']['stats'])
                engine_results_data = {k: EngineResults(**v) for k, v in analysis_response['data']['attributes']['results'].items()}
                return ScanAnalysisReport(stats=stats_data, results=engine_results_data)
            except KeyError:
                # Logging
                logger.error(f"KeyError: virus_total_analysis: {analysis_response}")
                raise HTTPException(status_code=500, detail="Unexpected response format from VirusTotal API")
            
    except httpx.HTTPStatusError as exc:
        # Logging
        logger.error(f"HTTPStatusError: virus_total_analysis {exc}")
        raise HTTPException(status_code=exc.response.status_code, detail="Error from VirusTotal API")
    
    except httpx.RequestError as exc:
        # Logging
        logger.error(f"RequestError: virus_total_analysis {exc}")
        raise HTTPException(status_code=500, detail=f"HTTP request failed: {exc}")