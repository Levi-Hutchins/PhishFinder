import json
import requests
import os
from dotenv import load_dotenv
import logging
from pydantic.tools import parse_obj_as
import json

from .mongo_service import insert_cloudflare_scan, get_uuid_from_url
from models.CloudFlareModels import CloudflareScanSubmission, CloudflareScanResult
from models.CloudflareFailedScan import FailedScan
from models.ModelRepository import URL_Link

logger = logging.getLogger("Link-ML-Service")
load_dotenv()

def url_cloudflare_submission(req: URL_Link) -> None:
    logger.task(f"Cloudflare submission: {req.link}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv("CLOUDFLARE_APIKEY")
    }
    payload = {"url": req.link}

    response = requests.post(os.getenv("CLOUDFLARE_URLSCAN_ENDPOINT"), headers=headers, json=payload)

    if response.status_code == 200:
        submission = CloudflareScanSubmission.model_validate(response.json())
        if insert_cloudflare_scan(submission):
            logger.info("Successful Cloudflare Submission")
    elif response.status_code == 409:
        logger.warning(f"Cloudflare Submission already queued for scanning {response.text}")
    else:
        logger.error(f"Request failed with status code {response.status_code} {response.text}")


def get_cloudflare_submission_result(url: str) -> CloudflareScanResult:
    print(url)
    uuid = get_uuid_from_url(url)

    if uuid == None: return None
    headers = {
        "Content-Type": "application/json",
        "Authorization": os.getenv("CLOUDFLARE_APIKEY")
    }
    print(uuid)
    scan_results = requests.get(os.getenv("CLOUDFLARE_RESULT_ENDPOINT")+uuid, headers=headers)
    print(scan_results.json())
    if scan_results.status_code == 200 and scan_results.json()['success'] == True:
        result = CloudflareScanResult.model_validate(scan_results.json())
        print(result)
        if result.result.scan["task"].status != "Finished":
            return "Scanning"
        else: 
            logger.info(f"Result fetched uuid: {uuid}")
            return result
    if scan_results.status_code == 200 and scan_results.json()['success'] == False:
        #print(scan_results.json())
        result = parse_obj_as(FailedScan, json.loads(scan_results.json()))
        print(result)

    
    





