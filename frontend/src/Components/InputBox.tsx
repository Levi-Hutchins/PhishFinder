import { TailSpin } from "react-loader-spinner";
import LinkModal from "../Modals/SubmitLinkModal";
import { UrlScanResponse, LinkPrediction, InputBoxProps } from "./Interfaces";
import React, { useState } from "react";
import Box from "@mui/material/Box";
import LinearProgress from "@mui/material/LinearProgress";

const InputBox: React.FC<InputBoxProps> = ({ onApiDataReceived }) => {
  const [inputValue, setInputValue] = useState("");
  const [urlLink, setUrlLink] = useState("");
  const [isLoading, setLoading] = useState(false);
  const [isFocused, setFocused] = useState(false);
  const [isModalOpen, setModalOpen]= useState(false);

  const handleFocused = () => {
    setFocused(true);
  };
  const handleBlur = () => {
    setFocused(false);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
    setUrlLink(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    // Add better UI feature for invalid URLs
    <LinkModal isOpen={isModalOpen} onClose={() => setModalOpen(false)} />
    if (urlLink == "") {
      alert("Please Enter Valid URL");
      return;
    }

    event.preventDefault();
    setLoading(true);
    console.log(JSON.stringify({ url_link: urlLink }));
    try {
      const virusTotalScan = await fetch(
        "http://127.0.0.1:8000/virus_total_urlscan/",
        {
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          method: "POST",

          mode: "cors",

          body: JSON.stringify({ url_link: urlLink }),
        }
      );

      if (!virusTotalScan.ok) {
        throw new Error(`Error: ${virusTotalScan.status}`);
      }
      const urlScanData: UrlScanResponse = await virusTotalScan.json();
      onApiDataReceived(urlScanData);

      console.log(urlScanData);
    } catch (error) {
      console.error("Oops Issue with request:", error);
      setLoading(false);
    }
    try {
      const linkPrediction = await fetch(
        "http://127.0.0.1:8000/link_prediction/",
        {
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          method: "POST",

          mode: "cors",

          body: JSON.stringify({ url_link: urlLink }),
        }
      );

      if (!linkPrediction.ok) {
        throw new Error(`Error: ${linkPrediction.status}`);
      }
      const modelPrediction: LinkPrediction = await linkPrediction.json();
      console.log(modelPrediction.status);
    } catch (error) {
      console.error("Oops Issue with request:", error);
      setLoading(false);
    }
    setLoading(false);
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        style={{ textAlign: "center", margin: "20px" }}
      >
        <div
          style={{
            position: "relative",
            display: "flex",
            alignItems: "center",
            border: isFocused ? "1px solid #bb86fc" : "1px solid #B1B1B1", // Change border color when focused
            borderRadius: "5px",
            overflow: "hidden", // Ensures that the children do not overflow the rounded corners
          }}
        >
          <input
            type="text"
            value={inputValue}
            onChange={handleChange}
            onFocus={handleFocused}
            onBlur={handleBlur}
            placeholder="Enter a URL"
            style={{
              color: "#f3f6f9",
              backgroundColor: "#222839",
              flex: 1, // Ensures input stretches to fill space
              //border: 'blue',
              padding: "10px", // Adjust padding as needed
              fontSize: "16px",
              height: "40px", // Adjust height as needed
              borderRadius: "5px", // Round the left corners only
              marginRight: "-150px", // Negative margin to account for button width

            }}
          />
          {isLoading ? (
            <></>
          ) : (
            <button
              type="submit"
              style={{
                marginTop: "8px",
                marginRight: "10px",
                width: "100px",
                height: "75%",
                border: "none",
                backgroundColor: "#7D48BD",
                color: "white",
                fontSize: "16px",
                cursor: "pointer",
                outline: "none",
                borderRadius: "5px", // Round the right corners only
                position: "absolute", // Keep the button positioned to the right
                top: "0", // Align to the top of the container
                right: "0", // Align to the right of the container
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.backgroundColor = "#5F378E";
                e.currentTarget.textContent = "Go Phish";
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.backgroundColor = "#7D48BD";
                e.currentTarget.textContent = "Scan URL";
              }}
              disabled={isLoading}
            >
              {isLoading ? (
                <TailSpin color="#00BFFF" height={20} width={20} />
              ) : (
                "Scan URL"
              )}
            </button>
          )}
        </div>
        <br />
        {isLoading ? (
          <Box sx={{ width: "50px%" }}>
            <LinearProgress color="secondary" />
          </Box>
        ) : (
          <></>
        )}
      </form>
    </>
  );
};

export default InputBox;
