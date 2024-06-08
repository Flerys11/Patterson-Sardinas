import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [source, setSource] = useState('');
  const [predictResult, setPredictResult] = useState(null);
  const [sdResult, setSdResult] = useState(null);

  const handleChange = (event) => {
    setSource(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const sourceArray = source.split(',').map(item => item.trim());
    
    try {
      const predictResponse = await axios.post('http://127.0.0.1:5000/predict', { source: sourceArray });
      setPredictResult(predictResponse.data.predictions);
    } catch (error) {
      console.error('Error fetching predictions:', error);
      setPredictResult(['Error fetching predictions']);
    }

    try {
      const sdResponse = await axios.post('http://127.0.0.1:5000/sd', { source: sourceArray });
      setSdResult(sdResponse.data['Resultats Sardinas Patterson']);
    } catch (error) {
      console.error('Error fetching Sardinas Patterson results:', error);
      setSdResult(['Error fetching Sardinas Patterson results']);
    }
  };

  return (
    <div className="App container">
      <header className="App-header">
        <h1 className="my-4">Code Classifier</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="mb-4">
          <div className="form-group row">
            <label htmlFor="binaryInput" className="col-sm-2 col-form-label">Entrer votre langage:</label>
            <div className="col-sm-10">
              <input
                type="text"
                className="form-control"
                id="binaryInput"
                value={source}
                onChange={handleChange}
                style={{ width: '100%' }}
              />
            </div>
          </div>
          <button type="submit" className="btn btn-primary mt-3">Verifier</button>
        </form>
        <div className="row">
        {predictResult && (
          <div className="col-md-6">
            <div className="results">
              <h2 className="mt-4">Reponse IA:</h2>
              <ul className="list-group">
                {predictResult.map((res, index) => (
                  <li 
                    key={index} 
                    className={`list-group-item ${String(res).toLowerCase() === 'true' ? 'text-green' : 'text-red'}`}
                  >
                    {String(res).toLowerCase() === 'true' ? 'CODE' : 'PAS CODE'}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      {sdResult !== null && (
        <div className="col-md-6">
          <div className="results">
            <h2 className="mt-4">Reponse Sardinas Patterson:</h2>
            <ul className="list-group">
              <li className={`list-group-item ${sdResult ? 'text-green' : 'text-red'}`}>
                {sdResult ? "CODE" : "PAS CODE"}
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>


      </main>
    </div>
  );
}

export default App;
