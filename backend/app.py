from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/apply_gate": {"origins": "http://localhost:3000"}})


# Define quantum gates
GATES = {
    "X": np.array([[0, 1], [1, 0]]),
    "H": np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])
}

@app.route('/apply_gate', methods=['POST'])
def apply_gate():
    data = request.json
    gate_name = data['gate']
    state_vector = np.array(data['state_vector'])
    
    if gate_name not in GATES:
        return jsonify({'error': 'Invalid gate'}), 400
    
    gate = GATES[gate_name]
    new_state = np.dot(gate, state_vector)
    
    # Round elements close to 0 or 1
    epsilon = 1e-10  # Threshold for rounding
    for i in range(len(new_state)):
        for j in range(len(new_state[i])):
            if abs(new_state[i][j] - 1) < epsilon:
                new_state[i][j] = 1
            elif abs(new_state[i][j]) < epsilon:
                new_state[i][j] = 0
    
    return jsonify({'new_state': new_state.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
