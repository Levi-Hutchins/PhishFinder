export interface UrlScanResponse {
    stats: UrlStats;
    results: EngineResults
    linkPrediction: string
}


export interface UrlStats {
    harmless: number;
    malicious: number;
    suspicity: number;
    undetected: number;
    timeout: number;

}

export interface EngineResults {
    [engineName: string]:{
        category: string;
        results: string;
        method: string;
        engine_name: string;
    }
}
export interface LinkPrediction{
    status: string;
}

export interface InputBoxProps {
    onApiDataReceived: (urlScanData: UrlScanResponse) => void; // Replace 'any' with a more specific type as needed
  }

export interface URLResultsProps{
    
    urlScanData: UrlScanResponse
}
