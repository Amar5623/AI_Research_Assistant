import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [summary, setSummary] = useState('');

  const handleSearch = async () => {
    const response = await axios.post('https://your-backend-api-url.com/summary', { query });
    setSummary(response.data.summary);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Powered Research Assistant</h1>
        <input 
          type="text" 
          value={query} 
          onChange={(e) => setQuery(e.target.value)} 
          placeholder="Enter your research query" 
        />
        <button onClick={handleSearch}>Search</button>
        {summary && <div className="summary"><h2>Summary</h2><p>{summary}</p></div>}
      </header>
    </div>
  );
}

export default App;
