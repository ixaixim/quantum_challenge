import React, { useState } from 'react';
import axios from 'axios';
import CircuitLine from './components/CircuitLine';
import GatePalette from './components/GatePalette';
import './App.css';

function App() {
  const [stateVector, setStateVector] = useState([[1], [0]]); // Initial state |0⟩

  const applyGate = (gate) => {
    axios.post('http://localhost:5000/apply_gate', {
      gate: gate,
      state_vector: stateVector
    }).then(response => {
      setStateVector(response.data.new_state);
    }).catch(error => {
      console.error('There was an error applying the gate!', error);
    });
  };

  return (
    <div className="App">
      <h1>Quantum Challenge</h1>
      <CircuitLine />
      <GatePalette applyGate={applyGate} />
      <div>
        <h2>Final State:</h2>
        <pre>{JSON.stringify(stateVector, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
