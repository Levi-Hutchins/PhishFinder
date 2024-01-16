from pydantic import BaseModel

class Email(BaseModel):
    subject: str
    title: str = None
    body: float
    #links: list(str)
    
class PhishingLink(BaseModel):
   url_link: str

class URLScanResponse:
    def __init__(self, data):
        self.type = data.get('type')
        self.id = data.get('id')
        self.self_link = data.get('links', {}).get('self')   


class EngineResults:
    def __init__(self, category, result, method, engine_name):
        self.category = category
        self.result = result
        self.method = method
        self.engine_name = engine_name

    def to_dict(self):
        return vars(self)

class Stats:
    def __init__(self, harmless, malicious, suspicious, undetected, timeout):
        self.harmless = harmless
        self.malicious = malicious
        self.suspicious = suspicious
        self.undetected = undetected
        self.timeout = timeout

    def to_dict(self):
        return vars(self)


class ScanAnalysisReport:
    def __init__(self, stats: Stats, results: EngineResults):
        self.stats: Stats = stats
        self.results: EngineResults = results

    def to_dict(self):
        return {
            "stats": self.stats,
            "results": {k: v for k, v in self.results.items()}
        }



