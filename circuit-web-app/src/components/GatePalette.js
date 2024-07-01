import React from 'react';
import '../css/GatePalette.css';

function GatePalette({ applyGate }) {
  return (
    <div className="gate-palette">
      <button onClick={() => applyGate('X')}>X Gate</button>
      <button onClick={() => applyGate('H')}>H Gate</button>
    </div>
  );
}

export default GatePalette;
