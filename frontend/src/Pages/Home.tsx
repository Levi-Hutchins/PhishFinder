import React from "react";
import SwimmingFish from "../Components/SwimmingFish";
import InputBox from "../Components/InputBox";
import "../Styles/App.css";
import { useState } from "react";
import URLResults from "../Components/URLResults";
import {
  UrlScanResponse,
  UrlStats,
  EngineResults,
} from "../Components/Interfaces";

const Home: React.FC = () => {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [urlAPIData, setUrlAPIData] = useState<UrlScanResponse>();

  const handleApiDataReceived = (data: UrlScanResponse) => {
    setUrlAPIData(data);
    setIsSubmitted(true);
  };

  console.log(urlAPIData?.stats);
  return (
    <>
      <header className="App-header">
        <SwimmingFish />
        <div className="title-container">
          <h2 className="phishguard-title">PhishFinder</h2>
          {!isSubmitted && (
            <InputBox onApiDataReceived={handleApiDataReceived} />
          )}
        </div>
      </header>
      {isSubmitted && urlAPIData && (
        // Render your new components here using the apiData
        <URLResults
          linkPrediction={urlAPIData.linkPrediction}
          stats={urlAPIData.stats}
          results={urlAPIData.results}
        />
      )}
    </>
  );
};

export default Home;
