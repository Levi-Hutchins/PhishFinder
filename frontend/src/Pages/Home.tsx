import React from "react"
import SwimmingFish from "../Components/SwimmingFish"
import InputBox from "../Components/InputBox"
import "../Styles/App.css"

const Home: React.FC = () => {

    return(
        <>
        
        <header className="App-header">
                <SwimmingFish/>

                <div className="title-container">
                <h2  className="phishguard-title">Catch-A-Phish</h2>

                <InputBox/>


                </div>
            </header>
        </>
    )
      

}
export default Home