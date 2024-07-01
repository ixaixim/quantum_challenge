import React, { useState } from 'react';
import '../css/GatePalette.css';

function GatePalette({ applyGate }) {
  const handleGateClick = (gate) => {
    applyGate(gate);
  };

  return (
    <div className="gate-palette">
      <button onClick={() => handleGateClick('X')}>X Gate</button>
      <button onClick={() => handleGateClick('H')}>H Gate</button>
    </div>
  );
}

export default GatePalette;
