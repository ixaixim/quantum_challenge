import streamlit as st
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt



# Define your page functions
def home_page():
    st.title("Home Page")
    st.write("Welcome to the Quantum Challenge!")


def generic_level(current_level):
    circuit = QuantumCircuit(1) if current_level < 3 else QuantumCircuit(2)
    # Initialize the session state for applied gates
    if 'applied_gates' not in st.session_state:
        st.session_state.applied_gates = []

    # Gate selection
    gate = st.selectbox('Select Gate', ['X', 'H']) if current_level < 3 else st.selectbox('Select Gate', ['X', 'H', 'CNOT'])

    # Apply gate button
    if st.button('Apply Gate'):
        st.session_state.applied_gates = apply_gate(gate, circuit, current_level, st.session_state.applied_gates)
        print("applied gates: ", st.session_state.applied_gates)
    
    # Display applied gates
    # st.write("Applied Gates:", st.session_state.applied_gates)

    # Check solution button
    if st.button('Check Solution'): 
        if check_solution(circuit, current_level, st.session_state.applied_gates):
            st.success("Congratulations! You've completed the level. Play the Next Level")
        else:
            st.error("The solution is not correct. Please try again.")        

    add_return_home_button()
    add_reset_button()

    cols = st.columns(2)
    cols[0].pyplot(draw_circuit(circuit, current_level, st.session_state.applied_gates))
    cols[1].pyplot(plot_statevector(circuit, current_level, st.session_state.applied_gates))

def level1_page():
    st.title("Level 1")
    st.write("Transform the qubit from |0⟩ to |1⟩ with a single gate.")
    generic_level(current_level=1)

def level2_page():
    st.title("Level 2")
    st.write("Create a superposition state of |0⟩ & |1⟩ with a single gate.")
    generic_level(current_level=2)

def level3_page():
    st.title("Level 3")
    st.write("Create a Bell state: |00⟩ + |11⟩ with two gates.")
    generic_level(current_level=3)

def end_page():
    st.title("End of Game")
    st.write("Congratulations! You've completed the Quantum Challenge!")
    st.image("winner.png")
    add_return_home_button()


# Utility function to add a return to home button
def add_return_home_button():
    if st.button("Return to Home"):
        st.query_params["page"] = "home"

def add_reset_button():
    if st.button("Reset"):
        st.session_state.applied_gates = []

#######################################################


# Helper functions
def apply_gate(gate, circuit, current_level, applied_gates):
    """
    Apply a selected gate to the quantum circuit.
    
    Parameters:
    gate (str): The gate to be applied ('X', 'H', 'CNOT').
    """
    if gate == "X":
        circuit.x(0)
        print('applied x gate in apply_gate')
    elif gate == "H":
        circuit.h(0)
    elif gate == "CNOT" and current_level >= 3:
        circuit.cx(0, 1)
    
    applied_gates.append(gate)
    return applied_gates

def check_solution(circuit, current_level, applied_gates):
    """
    Check if the applied gates result in the correct quantum state for the current level.
    
    Returns:
    bool: True if the solution is correct, otherwise False.
    """
    print("checking results... please wait")
    print("applied gates are: ", applied_gates)
    print("current level is: ", current_level)
    simulated_circuit = QuantumCircuit(1) if current_level < 3 else QuantumCircuit(2)
    for gate in applied_gates:
        if gate == "X":
            simulated_circuit.x(0)
        elif gate == "H":
            simulated_circuit.h(0)
        elif gate == "CNOT":
            simulated_circuit.cx(0, 1)
    print('------- printing simulated circuit -------\n')
    print(simulated_circuit.draw(output='text'))

    simulated_circuit.save_statevector()
    simulator = AerSimulator(method='statevector')
    compiled_circuit = transpile(simulated_circuit, simulator)
    sim_result = simulator.run(compiled_circuit).result()
    statevector = sim_result.get_statevector(compiled_circuit)

    solutions = {
        1: np.array([0, 1]),  # |1⟩
        2: np.array([1/np.sqrt(2), 1/np.sqrt(2)]),  # (|0⟩ + |1⟩) / sqrt(2)
        3: np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]),  # (|00⟩ + |11⟩) / sqrt(2)
    }

    target_state = solutions[current_level]
    statevector_np = np.array(statevector)

    target_probabilities = np.abs(target_state) ** 2
    state_probabilities = np.abs(statevector_np) ** 2
    print('target_probabilities: ', target_probabilities)
    print('state_probabilities: ', state_probabilities)
    simulated_circuit.data.clear()
    return np.allclose(state_probabilities, target_probabilities, atol=1e-2)

def draw_circuit(circuit, current_level, applied_gates):
    """
    Draw the quantum circuit with the applied gates.
    
    Returns:
    matplotlib.figure.Figure: The figure of the drawn quantum circuit.
    """
    print("------- inside draw circuit -------\n")
    simulated_circuit = QuantumCircuit(1) if current_level < 3 else QuantumCircuit(2)
    for gate in applied_gates:
        if gate == "X":
            simulated_circuit.x(0)
        elif gate == "H":
            simulated_circuit.h(0)
        elif gate == "CNOT":
            simulated_circuit.cx(0, 1)
    return circuit_drawer(simulated_circuit, output='mpl')

def plot_statevector(circuit, current_level, applied_gates):
    """
    Plot the statevector probabilities of the quantum circuit.
    
    Returns:
    matplotlib.figure.Figure: The figure of the statevector probabilities.
    """
    states = ['0', '1'] if current_level < 3 else ['00', '01', '10', '11']
    simulated_circuit = QuantumCircuit(1) if current_level < 3 else QuantumCircuit(2)
    for gate in applied_gates:
        if gate == "X":
            simulated_circuit.x(0)
        elif gate == "H":
            simulated_circuit.h(0)
        elif gate == "CNOT":
            simulated_circuit.cx(0, 1)
    simulator = AerSimulator(method='statevector')
    simulated_circuit.save_statevector()
    compiled_circuit = transpile(simulated_circuit, simulator)
    sim_result = simulator.run(compiled_circuit).result()
    statevector = sim_result.get_statevector(compiled_circuit)
    print("Statevector is:")
    print()
    print(statevector)
    probabilities = np.abs(statevector)**2
    
    fig, ax = plt.subplots()
    ax.bar(range(len(probabilities)), probabilities)
    ax.set_xlabel('State')
    ax.set_xticks(range(len(probabilities)))
    ax.set_xticklabels([f"|{i}⟩" for i in states])
    ax.set_ylabel('Probability')
    ax.set_title('Statevector Probabilities')
    simulated_circuit.data.clear()
    return fig

#######################################################
# Main
# Use URL parameters for page navigation
params = st.query_params
page = params.get("page", "home")

# Store the current page in session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# Reset applied gates if page changes
if page != st.session_state.current_page:
    st.session_state.applied_gates = []

# Initialize the session state for applied gates
if 'applied_gates' not in st.session_state:
    st.session_state.applied_gates = []

# Set the current page
st.session_state.current_page = page



def set_page(p):
    st.query_params["page"] = p

# Page routing
if page == "home":
    home_page()
    if st.button("Go to Level 1"):
        set_page("level1")
elif page == "level1":
    level1_page()
    if st.button("Go to Level 2"):
        set_page("level2")
elif page == "level2":
    level2_page()
    if st.button("Go to Level 3"):
        set_page("level3")
elif page == "level3":
    level3_page()
    if st.button("Go to End"):
        set_page("end")
elif page == "end":
    end_page()
