from pydantic import BaseModel, HttpUrl, validator
from typing import List, Optional

class ASN(BaseModel):
    asn: str
    description: str
    location_alpha2: str
    name: str
    org_name: str

class Certificate(BaseModel):
    issuer: str
    subjectName: str
    validFrom: int
    validTo: int

class Category(BaseModel):
    id: int
    name: str
    super_category_id: int

class DNS(BaseModel):
    address: str
    dnssec_valid: bool
    name: str
    type: str

class Rank(BaseModel):
    bucket: str
    name: str
    rank: int

class Domain(BaseModel):
    categories: Category
    dns: List[DNS]
    name: str
    rank: Rank
    type: str

class IP(BaseModel):
    asn: str
    asnDescription: str
    asnLocationAlpha2: str
    asnName: str
    asnOrgName: str
    continent: str
    geonameId: str
    ip: str
    ipVersion: str
    latitude: str
    locationAlpha2: str
    locationName: str
    longitude: str
    subdivision1Name: Optional[str]
    subdivision2Name: Optional[str]

class Link(BaseModel):
    href: HttpUrl
    text: str

class ProcessorCategory(BaseModel):
    content: List[Category]
    risks: List[Category]

class TechCategory(BaseModel):
    groups: List[int]
    id: int
    name: str
    priority: int
    slug: str

class Evidence(BaseModel):
    impliedBy: List[str]
    patterns: List[str]

class Tech(BaseModel):
    categories: List[TechCategory]
    confidence: int
    description: str
    evidence: Evidence
    icon: str
    name: str
    slug: str
    website: HttpUrl

class Processor(BaseModel):
    categories: ProcessorCategory
    phishing: List[str]
    rank: Rank
    tech: List[Tech]

class Page(BaseModel):
    asn: str
    asnLocationAlpha2: str
    asnname: str
    console: List[str]
    cookies: List[str]
    country: str
    countryLocationAlpha2: str
    domain: str
    headers: List[str]
    ip: str
    js: List[str]
    securityViolations: List[str]
    status: int
    subdivision1Name: Optional[str]
    subdivision2name: Optional[str]
    url: HttpUrl

class Performance(BaseModel):
    connectEnd: float
    connectStart: float
    decodedBodySize: int
    domComplete: int
    domContentLoadedEventEnd: float
    domContentLoadedEventStart: float
    domInteractive: float
    domainLookupEnd: float
    domainLookupStart: float
    duration: float
    encodedBodySize: int
    entryType: str
    fetchStart: float
    initiatorType: str
    loadEventEnd: float
    loadEventStart: float
    name: str
    nextHopProtocol: str
    redirectCount: int
    redirectEnd: float
    redirectStart: float
    requestStart: float
    responseEnd: float
    responseStart: float
    secureConnectionStart: float
    startTime: float
    transferSize: int
    type: str
    unloadEventEnd: float
    unloadEventStart: float
    workerStart: float

class Task(BaseModel):
    clientLocation: str
    clientType: str
    effectiveUrl: HttpUrl
    errors: List[str]
    scannedFrom: str
    status: str
    success: bool
    time: str
    timeEnd: str
    url: HttpUrl
    uuid: str
    visibility: str

class Verdict(BaseModel):
    categories: List[Category]
    malicious: bool
    phishing: List[str]

class Scan(BaseModel):
    asns: ASN
    domains: Domain
    geo: IP
    ips: IP
    meta: Processor
    task: Task
    verdicts: Verdict

class Error(BaseModel):
    message: str

class Message(BaseModel):
    message: str

class Result(BaseModel):
    scan: Scan

class Response(BaseModel):
    errors: List[Error]
    messages: List[Message]
    result: Result
    success: bool
