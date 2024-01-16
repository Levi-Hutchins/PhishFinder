import React from 'react';
import InputBox  from './Components/InputBox'
import './App.css';

function App() {
  return (
    <div className="App">
      
      <header className="App-header">
        <div className="title-container">
        <h2  className="phishguard-title">PhishGuard</h2>
        <InputBox/>
        </div>
      </header>
    </div>
  );
}

export default App;
