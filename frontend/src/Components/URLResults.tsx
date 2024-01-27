import React from "react"
import { UrlScanResponse } from "./Interfaces"

const URLResults: React.FC<UrlScanResponse> = ({linkPrediction,stats,results}) =>{
    return(
        <>

        <p>

            {stats.harmless}
        </p>

        </>
    )
}

export default URLResults
