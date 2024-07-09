import json
import requests
import os
from dotenv import load_dotenv
import logging

from .mongo_service import insert_cloudflare_scan
from models.CloudFlareModels import CloudflareScanSubmission
from models.ModelRepository import URL_Link

logger = logging.getLogger("Link-ML-Service")
load_dotenv()

def url_cloudflare_submission(req:URL_Link):

    logger.task(f"Cloudflare submission: {req.link}")

    headers = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("CLOUDFLARE_APIKEY")
    }
    payload = {"url": req.link}
    response = requests.post(os.getenv("CLOUDFLARE_URLSCAN_ENDPOINT"), headers=headers, json=payload)

    if response.status_code == 200:
        submission = CloudflareScanSubmission.model_validate(json.loads(response.text))
        insert_cloudflare_scan(submission)
        logger.info("Successful Cloudflare Submission")
    else:
        logger.error(f"Request failed with status code {response.status_code} {response.text}")
