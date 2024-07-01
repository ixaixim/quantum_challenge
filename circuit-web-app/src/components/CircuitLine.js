import React from 'react';
import '../css/CircuitLine.css';

function CircuitLine({ gates }) {
    console.log(gates); 
  const renderGates = () => {
    return gates.map((gate, index) => (
      <text key={index} x={50 + (gate.position * 100)} y={50} fill="black" fontSize="20" textAnchor="middle">
        {gate.gate}
      </text>
    ));
  };

  return (
    <div className="circuit-line">
      <svg width="400" height="100">
        <line x1="50" y1="50" x2="350" y2="50" stroke="black" strokeWidth="2" />
        {renderGates()}
      </svg>
    </div>
  );
}

export default CircuitLine;
