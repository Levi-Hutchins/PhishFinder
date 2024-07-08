import json
import requests
import os
from dotenv import load_dotenv
import logging
from models.CloudFlareModels import CloudflareScanSubmission
from models.ModelRepository import URL_Link
load_dotenv()

logger = logging.getLogger("Link-ML-Service")
def url_cloudflare_submission(req:URL_Link):

    logger.task(f"Cloudflare submission: {req.link}")

    headers = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("CLOUDFLARE_APIKEY")
    }
    payload = {"url": req.link}
    print("here2")
    response = requests.post(os.getenv("CLOUDFLARE_URLSCAN_ENDPOINT"), headers=headers, json=payload)

    if response.status_code == 200:
        url_result = CloudflareScanSubmission.model_validate(json.loads(response.text))
        print(url_result)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)