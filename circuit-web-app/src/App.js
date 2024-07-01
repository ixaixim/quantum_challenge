import React, { useState } from 'react';
import axios from 'axios';
import CircuitLine from './components/CircuitLine';
import GatePalette from './components/GatePalette';
import './App.css';

function App() {
  const [stateVector, setStateVector] = useState([[1], [0]]); // Initial state |0⟩
  const [gates, setGates] = useState([]);
  const [position, setPosition] = useState(0);


const applyGate = (gate, position) => {
    console.log(`Applying ${gate} gate at position ${position}`); // Added console log
    axios.post('http://localhost:5000/apply_gate', {
      gate: gate,
      state_vector: stateVector
    }).then(response => {
      setStateVector(response.data.new_state);
      setGates([...gates, { gate, position }]);
      setPosition(position + 1); // Update position for next gate
    }).catch(error => {
      console.error('There was an error applying the gate!', error);
    });
  };
  const resetCircuit = () => {
    setStateVector([[1], [0]]); // Reset to initial state |0⟩
    setGates([]); // Clear all gates
    setPosition(0); // Reset position
  };


  return (
    <div className="App">
      <h1>Quantum Challenge</h1>
      <CircuitLine gates={gates} />
      <GatePalette applyGate={applyGate} />
      <div>
        <h2>Final State:</h2>
        <pre>{JSON.stringify(stateVector, null, 2)}</pre>
      </div>
      <button onClick={resetCircuit} className="reset-button">Reset</button>
    </div>
  );
}

export default App;
