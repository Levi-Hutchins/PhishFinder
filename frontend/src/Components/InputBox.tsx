import { TailSpin } from "react-loader-spinner";
import { UrlScanResponse } from "./Interfaces";
import React, { useState } from "react";


const InputBox: React.FC = () => {
  const [inputValue, setInputValue] = useState("");
  const [urlLink, setUrlLink] = useState("");
  const [isLoading, setLoading] = useState(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
    setUrlLink(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    console.log(JSON.stringify({ url_link: urlLink }))
    try {
      const response = await fetch("http://127.0.0.1:8000/virus_total_urlscan/", 
      {
        headers: {
            'Accept': 'application/json',
            "Content-Type": "application/json"
          },
        method: "POST",

        mode: "cors",
        
        body: JSON.stringify({ url_link: urlLink }),
    });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const urlScanData: UrlScanResponse = await response.json();
      setLoading(false);
      console.log(urlScanData.stats);


      // Handle response data
      
    } catch (error) {
      console.error("Oops Issue with request:", error);
      setLoading(false);
    }

  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        style={{ textAlign: "center", margin: "20px" }}
      >
        <input
          type="text"
          value={inputValue}
          onChange={handleChange}
          placeholder="Enter your password"
          style={{
            width: "100%",
            height: "50px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            padding: "5px 10px",
            fontSize: "16px",
            margin: "10px 0",
          }}
        />
        <br />
        <button
          type="submit"
          style={{
            width: "150px",
            height: "40px",
            borderRadius: "5px",
            border: "none",
            backgroundColor: "#007bff",
            color: "white",
            fontSize: "16px",
            cursor: "pointer",
            outline: "none",
            position: "relative", // Add this to handle positioning
          }}
          onMouseOver={(e) =>
            (e.currentTarget.style.backgroundColor = "#0056b3")
          }
          onMouseOut={(e) =>
            (e.currentTarget.style.backgroundColor = "#007bff")
          }
          disabled={isLoading} // Disable the button when loading
        >
          {isLoading ? (
            <div
              style={{
                position: "absolute",
                left: "50%",
                top: "50%",
                transform: "translate(-50%, -50%)",
              }}
            >
              <TailSpin color="#00BFFF" height={40} width={40} />
            </div>
          ) : (
            "Calculate"
          )}
        </button>
      </form>
    </>
  );
};

export default InputBox;
