import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from config.API_KEYS import VIRUS_TOTAL
from scripts import url_processing, model_prediction
from models import PhishingLink, PredictionResponse,URLScanResponse,EngineResults, Stats, ScanAnalysisReport

app = FastAPI()

def get_api_headers(reference_code: int, user_req: PhishingLink):
    if reference_code == 0:
        url = "https://www.virustotal.com/api/v3/urls"
        payload = {"url": user_req.url_link}
        headers = {
            "accept": "application/json",
            "x-apikey": VIRUS_TOTAL
        }
        return url, payload, headers



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
    url, payload, headers = get_api_headers(0, user_req)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload, headers=headers)
            response.raise_for_status()

            try:
                user_requested_url = URLScanResponse(id=response.json()["data"]["id"])
            except KeyError:
                # Logging
                raise HTTPException(status_code=500, detail="Unexpected response format from VirusTotal API")

            analysis_report: ScanAnalysisReport = await virus_total_analysis(user_requested_url)
        return analysis_report.model_dump()
    except httpx.HTTPStatusError as exc:
        # Logging
        raise HTTPException(status_code=exc.response.status_code, detail="Error from VirusTotal API")
    
    except httpx.RequestError as exc:
        # Logging
        raise HTTPException(status_code=500, detail=f"HTTP request failed: {exc}")

async def virus_total_analysis(scanned_url: URLScanResponse):
    url = f"https://www.virustotal.com/api/v3/analyses/{scanned_url.id}"
    headers = {
    "accept": "application/json",
    "x-apikey": VIRUS_TOTAL
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from VirusTotal API")

        analysis_response = response.json()
        stats_data = Stats(**analysis_response['data']['attributes']['stats'])
        engine_results_data = {k: EngineResults(**v) for k, v in analysis_response['data']['attributes']['results'].items()}
        analysis_report = ScanAnalysisReport(stats=stats_data, results=engine_results_data)
        return analysis_report