import React, { useRef, useEffect } from "react";
import video from "../assets/bg_vid.mp4";
import "../Styles/Video.css";
import "@fontsource/archivo-black"; 
import "../Styles/Home.css"
import InputBox from "../Components/InputBox/InputBoxv2";

const Home: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement>(null);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.playbackRate = 0.9; // Set playback speed to 0.5x
    }
  }, []);

  return (
    <div className="main">
      <div className="overlay"></div>
      <video ref={videoRef} src={video} autoPlay loop muted />
      <h1 className="phishfinder-title-PHISH">Phish</h1>
      <h1 className="phishfinder-title-FINDER">Finder</h1>
      <InputBox/>
    </div>
  );
};

export default Home;
