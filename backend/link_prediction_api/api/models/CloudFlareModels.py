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



class ResultMessage(BaseModel):
    message: Optional[str] = None

class Task(BaseModel):
    uuid: Optional[str] = None
    url: Optional[str] = None
    effectiveUrl: Optional[str] = None
    status: Optional[str] = None
    time: Optional[str] = None
    visibility: Optional[str] = None
    clientLocation: Optional[str] = None
    clientType: Optional[str] = None
    extraOptions: Optional[Dict[str, Any]] = None
    scannedFrom: Optional[Dict[str, Any]] = None
    timeEnd: Optional[str] = None
    errors: Optional[List[Any]] = None
    success: Optional[bool] = None
    serverASN: Optional[str] = None
    serverLocation: Optional[str] = None

class ServerTiming(BaseModel):
    name: Optional[str] = None
    duration: Optional[float] = None
    description: Optional[str] = None

class Performance(BaseModel):
    name: Optional[str] = None
    entryType: Optional[str] = None
    startTime: Optional[float] = None
    duration: Optional[float] = None
    initiatorType: Optional[str] = None
    renderBlockingStatus: Optional[str] = None
    workerStart: Optional[float] = None
    redirectStart: Optional[float] = None
    redirectEnd: Optional[float] = None
    fetchStart: Optional[float] = None
    domainLookupStart: Optional[float] = None
    domainLookupEnd: Optional[float] = None
    connectStart: Optional[float] = None
    secureConnectionStart: Optional[float] = None
    connectEnd: Optional[float] = None
    requestStart: Optional[float] = None
    responseStart: Optional[float] = None
    firstInterimResponseStart: Optional[float] = None
    responseEnd: Optional[float] = None
    transferSize: Optional[int] = None
    encodedBodySize: Optional[int] = None
    decodedBodySize: Optional[int] = None
    responseStatus: Optional[int] = None
    serverTiming: Optional[List[ServerTiming]] = None
    unloadEventStart: Optional[float] = None
    unloadEventEnd: Optional[float] = None
    domInteractive: Optional[float] = None
    domContentLoadedEventStart: Optional[float] = None
    domContentLoadedEventEnd: Optional[float] = None
    domComplete: Optional[float] = None
    loadEventStart: Optional[float] = None
    loadEventEnd: Optional[float] = None
    type: Optional[str] = None
    redirectCount: Optional[int] = None
    activationStart: Optional[float] = None
    criticalCHRestart: Optional[float] = None

class MetaProcessor(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    categories: Optional[List[Dict[str, Any]]] = None
    confidence: Optional[int] = None
    version: Optional[str] = None
    icon: Optional[str] = None
    website: Optional[str] = None
    pricing: Optional[List[str]] = None
    cpe: Optional[str] = None
    match: Optional[Dict[str, Any]] = None
    evidence: Optional[Dict[str, Any]] = None

class MetaCategory(BaseModel):
    id: Optional[int] = None
    super_category_id: Optional[int] = None
    name: Optional[str] = None

class MetaRank(BaseModel):
    name: Optional[str] = None
    bucket: Optional[str] = None
    rank: Optional[int] = None

class Meta(BaseModel):
    processors: Optional[Dict[str, List[MetaProcessor]]] = None
    categories: Optional[Dict[str, List[MetaCategory]]] = None
    rank: Optional[MetaRank] = None
    phishing: Optional[List[Any]] = None

class Domain(BaseModel):
    name: Optional[str] = None
    categories: Optional[Dict[str, Any]] = None
    dns: Optional[List[Dict[str, Any]]] = None
    type: Optional[str] = None
    rank: Optional[Dict[str, Any]] = None

class IP(BaseModel):
    ip: Optional[str] = None
    ipVersion: Optional[str] = None
    locationAlpha2: Optional[str] = None
    locationName: Optional[str] = None
    subdivision1Name: Optional[str] = None
    subdivision2Name: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    continent: Optional[str] = None
    geonameId: Optional[str] = None
    asn: Optional[str] = None
    asnName: Optional[str] = None
    asnOrgName: Optional[str] = None
    asnDescription: Optional[str] = None
    asnLocationAlpha2: Optional[str] = None

class PageHistory(BaseModel):
    url: Optional[str] = None
    statusCode: Optional[int] = None
    uuid: Optional[str] = None

class Certificate(BaseModel):
    issuer: Optional[str] = None
    subjectName: Optional[str] = None
    validFrom: Optional[int] = None
    validTo: Optional[int] = None

class JSVariable(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None

class ConsoleEntry(BaseModel):
    type: Optional[str] = None
    text: Optional[str] = None
    category: Optional[str] = None
    url: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None

class Cookie(BaseModel):
    name: Optional[str] = None
    value: Optional[str] = None
    domain: Optional[str] = None
    path: Optional[str] = None
    expires: Optional[float] = None
    size: Optional[int] = None
    httpOnly: Optional[bool] = None
    secure: Optional[bool] = None
    session: Optional[bool] = None
    sameSite: Optional[str] = None
    priority: Optional[str] = None
    sameParty: Optional[bool] = None
    sourceScheme: Optional[str] = None
    sourcePort: Optional[int] = None

class Page(BaseModel):
    url: Optional[str] = None
    domain: Optional[str] = None
    country: Optional[str] = None
    countryLocationAlpha2: Optional[str] = None
    subdivision1Name: Optional[str] = None
    subdivision2Name: Optional[str] = None
    ip: Optional[str] = None
    asn: Optional[str] = None
    asnname: Optional[str] = None
    asnLocationAlpha2: Optional[str] = None
    cookies: Optional[List[Cookie]] = None
    headers: Optional[List[Dict[str, str]]] = None
    status: Optional[int] = None
    server: Optional[str] = None
    mimeType: Optional[str] = None
    title: Optional[str] = None
    apexDomain: Optional[str] = None
    ptr: Optional[str] = None
    certificate: Optional[Certificate] = None
    js: Optional[Dict[str, List[JSVariable]]] = None
    console: Optional[List[ConsoleEntry]] = None
    securityViolations: Optional[List[Any]] = None

class Stats(BaseModel):
    domains: Optional[int] = None
    geo: Optional[Dict[str, int]] = None
    asns: Optional[int] = None
    ips: Optional[Dict[str, int]] = None
    cookies: Optional[int] = None
    links: Optional[int] = None
    requests: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None

class Verdicts(BaseModel):
    overall: Optional[Dict[str, Any]] = None

class Hashes(BaseModel):
    hashes: Optional[List[str]] = None

class ScanResult(BaseModel):
    scan: Optional[Dict[str, Task]] = None
    performance: Optional[List[Performance]] = None
    cookies: Optional[List[Any]] = None
    meta: Optional[Meta] = None
    domains: Optional[Dict[str, Domain]] = None
    ips: Optional[Dict[str, IP]] = None
    pageHistory: Optional[List[PageHistory]] = None
    page: Optional[Page] = None
    asns: Optional[Dict[str, Any]] = None
    geo: Optional[Dict[str, Any]] = None
    links: Optional[Dict[str, Any]] = None
    certificates: Optional[List[Certificate]] = None
    stats: Optional[Stats] = None
    verdicts: Optional[Verdicts] = None
    hashes: Optional[Hashes] = None

class CloudflareScanResult(BaseModel):
    success: Optional[bool] = None
    messages: Optional[List[ResultMessage]] = None
    result: Optional[ScanResult]