import logging
import json
import requests
import os
from dotenv import load_dotenv

from models import ModelLinkReq
from models.CloudFlareModels import CloudflareScanSubmission
logger = logging.getLogger("Link-ML-Service")
load_dotenv()

def url_cloudflare_submission(req:ModelLinkReq):
    logger.info("[TASK] Cloudflare URLScan")
    headers = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("CLOUDFLARE_APIKEY")
    }
    payload = {"url": req.url_link}

    response = requests.post(os.getenv("CLOUDFLARE_URLSCAN_ENDPOINT"), headers=headers, json=payload)

    if response.status_code == 200:
        url_result = CloudflareScanSubmission.model_validate(json.loads(response.text))
        print(url_result)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)