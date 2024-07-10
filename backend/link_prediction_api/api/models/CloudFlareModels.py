from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class SubmissionMessage(BaseModel):
    message: str

class SubmissionResult(BaseModel):
    visibility: str
    uuid: str
    url: str
    time: datetime

class CloudflareScanSubmission(BaseModel):
    success: bool
    messages: List[SubmissionMessage]
    result: Optional[SubmissionResult] = None
    errors: List[str]



class Task(BaseModel):
    uuid: str
    url: str
    effectiveUrl: str
    status: str
    time: str
    visibility: str
    clientLocation: str
    clientType: str
    timeEnd: str
    errors: List[Any]
    success: bool
    serverASN: str
    serverLocation: str

class Performance(BaseModel):
    name: str
    entryType: str
    startTime: float
    duration: float
    initiatorType: str
    renderBlockingStatus: str
    workerStart: float
    redirectStart: float
    redirectEnd: float
    fetchStart: float
    domainLookupStart: float
    domainLookupEnd: float
    connectStart: float
    secureConnectionStart: float
    connectEnd: float
    requestStart: float
    responseStart: float
    firstInterimResponseStart: float
    responseEnd: float
    transferSize: int
    encodedBodySize: int
    decodedBodySize: int
    responseStatus: int
    serverTiming: List[Any]
    unloadEventStart: float
    unloadEventEnd: float
    domInteractive: float
    domContentLoadedEventStart: float
    domContentLoadedEventEnd: float
    domComplete: float
    loadEventStart: float
    loadEventEnd: float
    type: str
    redirectCount: int
    activationStart: float
    criticalCHRestart: float

class MetaProcessor(BaseModel):
    name: str
    description: str
    slug: str
    categories: List[Dict[str, Any]]
    confidence: int
    version: str
    icon: str
    website: str
    pricing: List[str]
    cpe: Optional[str]
    match: Dict[str, Any]
    evidence: Dict[str, Any]

class MetaCategory(BaseModel):
    id: int
    super_category_id: int
    name: str

class MetaRank(BaseModel):
    name: str
    bucket: str
    rank: int

class Meta(BaseModel):
    processors: Dict[str, List[MetaProcessor]]
    categories: Dict[str, List[MetaCategory]]
    rank: MetaRank
    phishing: List[Any]

class Domain(BaseModel):
    name: str
    categories: Dict[str, Any]
    dns: List[Dict[str, Any]]
    type: Optional[str]
    rank: Optional[Dict[str, Any]]

class IP(BaseModel):
    ip: str
    ipVersion: str
    locationAlpha2: str
    locationName: str
    subdivision1Name: str
    subdivision2Name: Optional[str]
    latitude: str
    longitude: str
    continent: str
    geonameId: str
    asn: str
    asnName: str
    asnOrgName: str
    asnDescription: str
    asnLocationAlpha2: str

class PageHistory(BaseModel):
    url: str
    statusCode: int
    uuid: str

class Certificate(BaseModel):
    issuer: str
    subjectName: str
    validFrom: int
    validTo: int

class JSVariable(BaseModel):
    name: str
    type: str

class ConsoleEntry(BaseModel):
    type: str
    text: str
    category: str
    url: str

class Page(BaseModel):
    url: str
    domain: str
    country: str
    countryLocationAlpha2: str
    subdivision1Name: str
    subdivision2Name: Optional[str]
    ip: str
    asn: str
    asnname: str
    asnLocationAlpha2: str
    cookies: List[Any]
    headers: List[Dict[str, str]]
    status: int
    server: str
    mimeType: str
    title: str
    apexDomain: str
    ptr: str
    certificate: Certificate
    js: Dict[str, List[JSVariable]]
    console: List[ConsoleEntry]
    securityViolations: List[Any]

class Stats(BaseModel):
    domains: int
    geo: Dict[str, int]
    asns: int
    ips: Dict[str, int]
    cookies: int
    links: int
    requests: Dict[str, Any]
    meta: Dict[str, Any]

class Verdicts(BaseModel):
    overall: Dict[str, Any]

class Hashes(BaseModel):
    hashes: List[str]

class ScanResult(BaseModel):
    scan: Dict[str, Task]
    performance: List[Performance]
    cookies: List[Any]
    meta: Meta
    domains: Dict[str, Domain]
    ips: Dict[str, IP]
    pageHistory: List[PageHistory]
    page: Page
    asns: Dict[str, Any]
    geo: Dict[str, Any]
    links: Dict[str, Any]
    certificates: List[Certificate]
    stats: Stats
    verdicts: Verdicts
    hashes: Hashes

class ResultMessage(BaseModel):
    message: str

class CloudflareScanResult(BaseModel):
    success: bool
    messages: List[ResultMessage]
    result: ScanResult
    errors: List[Any]