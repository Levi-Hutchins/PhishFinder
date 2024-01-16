export interface UrlScanResponse {
    stats: UrlStats;
    reuslts: EngineResults
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
