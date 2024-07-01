import React from 'react';
import '../css/CircuitLine.css';

function CircuitLine() {
  return (
    <div className="circuit-line">
      <svg width="400" height="100">
        <line x1="50" y1="50" x2="350" y2="50" stroke="black" strokeWidth="2" />
      </svg>
    </div>
  );
}

export default CircuitLine;
