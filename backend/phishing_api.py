import httpx
import html

import validators

import re
import bleach

from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException

from scripts.config.API_KEYS import VIRUS_TOTAL

from scripts import url_processing, model_prediction

from models import PhishingLink, PredictionResponse,URLScanResponse,EngineResults, Stats, ScanAnalysisReport

app = FastAPI()

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

def validate_url(unvalidated_url: str) -> bool:
    contains_escapedChars = r'&[#]?[a-zA-Z0-9]+;'
    # Need to investiage more validation methods 
    # Perform multiple validations to prevent false urls

    isvalid_1 = validators.url(unvalidated_url)
    isvalid_2 = re.match(contains_escapedChars, unvalidated_url)
    if isvalid_1 and isvalid_2: return True
    else: return False





def clean_url(unclean_url: str) -> str:

    clean_layer_1 = bleach.clean(unclean_url)
    clean_layer_2 = html.escape(clean_layer_1)

    return clean_layer_2


@app.post("/link_prediction/")
async def inhouse_model_prediction(user_req: PhishingLink):
    x_labels = url_processing.get_url_prediction_values(user_req.url_link)

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
    if validate_url(unvalidated_url):
    
    
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
                    # Logging
                    print(f"KeyError: /virus_total_urlscan/: Request URL = {user_requested_url}")
                    raise HTTPException(status_code=500, detail="Unexpected response format from VirusTotal API")

                analysis_report: ScanAnalysisReport = await virus_total_analysis(user_requested_url)
            return analysis_report.model_dump()
        except httpx.HTTPStatusError as exc:
            # Logging
            print(f"HTTPStatusError: /virus_total_urlscan/  {exc}")
            raise HTTPException(status_code=exc.response.status_code, detail="Error from VirusTotal API")
        
        except httpx.RequestError as exc:
            # Logging
            print(f"RequestError: /virus_total_urlscan/  {exc}")
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
                print(f"KeyError: virus_total_analysis: {analysis_response}")
                raise HTTPException(status_code=500, detail="Unexpected response format from VirusTotal API")
            
    except httpx.HTTPStatusError as exc:
        # Logging
        print(f"HTTPStatusError: virus_total_analysis {exc}")
        raise HTTPException(status_code=exc.response.status_code, detail="Error from VirusTotal API")
    
    except httpx.RequestError as exc:
        # Logging
        print(f"RequestError: virus_total_analysis {exc}")
        raise HTTPException(status_code=500, detail=f"HTTP request failed: {exc}")
        

            