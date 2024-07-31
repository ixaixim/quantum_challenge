import streamlit as st
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-interactive environments




# Define your page functions
def home_page():

    st.markdown(
        """
        <div style='text-align: center; font-size: 24px;'>
            <h1>Welcome to the VW Quantum Challenge 😊</h1>
            <h2>Take a break at our desk,</h2>
            <h2>Play the game and win some 🍬🍭.</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h2>Instructions</h2>", unsafe_allow_html=True)
    add_explanation_button()
    add_tutorial_button()
    # Displaying an image
    # st.image("quantum_computer_home.jpg", width=500)

    st.markdown("<h2>Play now</h2>", unsafe_allow_html=True)

def explanation_page(): 
    st.markdown(
        "<div style='text-align: center;'><h1>Quantum Challenge Tutorial</h1></div>",
        unsafe_allow_html=True
    )
    
    st.markdown("<h2>Objective</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:24px;'>Complete the quantum circuits for each level by applying the correct gates.</p>", 
        unsafe_allow_html=True
    )
    
    st.markdown("<h2>Definitions</h2>", unsafe_allow_html=True)
    
    st.markdown("<h3>Bit and Qubit</h3>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:24px;'>A bit is like a tiny switch that can either be off (denoted by <b>|0⟩</b>) or on (denoted by <b>|1⟩</b>).</p>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:24px;'><b>|0⟩</b> and <b>|1⟩</b> represent two states. For example, the bit <b>|0⟩</b> corresponds to a neutral face, while <b>|1⟩</b> corresponds to a smiling face: <br><b>|0⟩ = 😐, |1⟩ = 😃</b></p>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:24px;'>A qubit, however, is a more complex unit of information that can be in state <b>|0⟩</b>, <b>|1⟩</b>, or any combination of both, simultaneously.</p>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:24px;'>This superposition is like being both happy and neutral, resulting in a confused state: <br><b>|0⟩ = 😐, |1⟩ = 😃, (|0⟩ + |1⟩) = 😵</b></p>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:24px;'>We hope you are not confused and are ready to dive into quantum gates!</p>",
        unsafe_allow_html=True
    )

    st.image("superposition.jpg", caption='Superposition of two states is possible in quantum computing. One object can be in two states at the same time.', use_column_width=True)
    
    st.markdown("<h3>Gates</h3>", unsafe_allow_html=True)   
    st.markdown(
        "<p style='font-size:24px;'>Gates are tools that manipulate bits or qubits in specific ways.</p>", 
        unsafe_allow_html=True
    )   
    st.markdown("<h4>X Gate</h4>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:24px;'>The X gate flips a bit or qubit from <b>|0⟩</b> to <b>|1⟩</b> and vice versa.</p>", 
        unsafe_allow_html=True
    )
    st.markdown("<h4>Hadamard (H) Gate</h4>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:24px;'>The Hadamard gate places a qubit into a superposition of <b>|0⟩</b> and <b>|1⟩</b> states.</p>", 
        unsafe_allow_html=True
    )
    st.markdown("<h4>CNOT Gate</h4>", unsafe_allow_html=True)

    st.markdown(
        "<p style='font-size:24px;'>The CNOT gate creates an entangled state between two qubits, linking their states.</p>", 
        unsafe_allow_html=True
    )





    st.markdown("Developed with ❤️ by the VW Quantum Team Doctorands, Neel Misciasci and Chinonso Calistus Onah")


def tutorial_page():

    st.markdown("<h2>How to Play</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:24px;'>Your task is to create a quantum algorithm by selecting the gates and applying them to the quantum circuit.</p>", 
            unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size:24px;'>1. Select a gate from the dropdown menu.</p>", 
        unsafe_allow_html=True
    )
    st.image("select-gate.png", caption='Image Caption', use_column_width=True)

    st.markdown(
        "<p style='font-size:24px;'>2. Click the 'Apply Gate' button to apply the selected gate to the quantum circuit. If you mess up, you can always reset the game.</p>", 
        unsafe_allow_html=True
    )
    st.image("apply-gate.png", caption='Apply gate or Reset the game', use_column_width=True)

    st.markdown(
        "<p style='font-size:24px;'>3. You can see the result of your actions by looking at the quantum circuit (on the left) and the probable results (on the right).</p>",
        unsafe_allow_html=True
    )
    st.image("quantum_circuit_probs.png", caption='This quantum circuit has two X gates, the result is |0> with maximum probability', use_column_width=True)
    st.markdown(
        "<p style='font-size:24px;'>4. Solve the task and proceed to the next level!</p>", 
        unsafe_allow_html=True
    )
    st.image("pass_level.png", caption='Completed game.', use_column_width=True) 
    st.markdown(
        "<p style='font-size:24px;'>5. Have fun! If you win the three levels, you can take a piece of 🍬🍭. You deserved it!</p>", 
        unsafe_allow_html=True
    )

    st.markdown("Developed with ❤️ by the VW Quantum Team Doctorands, Neel Misciasci and Chinonso Calistus Onah")





def generic_level(current_level):
    circuit = QuantumCircuit(1) if current_level < 3 else QuantumCircuit(2)
    # Initialize the session state for applied gates
    if 'applied_gates' not in st.session_state:
        st.session_state.applied_gates = []

    # Gate selection

    # Example selectbox with different options based on the level
    gate = st.selectbox('Select Gate', ['X', 'H']) if current_level < 3 else st.selectbox('Select Gate', ['X', 'H', 'CNOT'])

    # Apply gate button

    # Create two columns for the buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button('Apply Gate'):
            st.session_state.applied_gates = apply_gate(gate, circuit, current_level, st.session_state.applied_gates)
            print("Applied gates:", st.session_state.applied_gates)
        
        # Centering the button in the column
        col1.markdown("<style>div.stButton > button {display: block; margin: 0 auto;}</style>", unsafe_allow_html=True)

    with col2:
        # Assuming add_reset_button is a function defined elsewhere to add a reset button
        add_reset_button()
        
        # Centering the button in the column
        col2.markdown("<style>div.stButton > button {display: block; margin: 0 auto;}</style>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    cols = st.columns(2)
    cols[0].pyplot(draw_circuit(circuit, current_level, st.session_state.applied_gates))
    cols[1].pyplot(plot_statevector(circuit, current_level, st.session_state.applied_gates))
    
    # Check solution button
    # if st.button('Check Solution'): 
    st.markdown(
        """
        <style>
        .message-box {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            border-radius: 5px;
            border: 2px solid;
            margin: 20px;
            text-align: center;
            font-size: 24px;
            color: black; /* Text color */
        }
        .success-box {
            background-color: #ccffcc; /* Light green background */
            border-color: #33cc33; /* Darker green border */
        }
        .error-box {
            background-color: #ffcccc; /* Light red background */
            border-color: #ff3333; /* Darker red border */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if check_solution(circuit, current_level, st.session_state.applied_gates):
        st.markdown(
            '<div class="message-box success-box">Congratulations! You\'ve completed the level. Play the Next Level (button below)</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="message-box error-box">The solution is not correct. Please try again.</div>', 
            unsafe_allow_html=True
        )


    add_return_home_button()

def level1_page():
    st.title("Level 1: X Gate")
    st.write("")
    st.markdown(
    "<p style='font-size:24px;'>Transform the qubit from |0⟩ to |1⟩ with a single gate.</p>", 
    unsafe_allow_html=True
    )

    generic_level(current_level=1)

def level2_page():
    st.title("Level 2: Hadamard Gate")
    st.markdown(
    "<p style='font-size:24px;'>Create a superposition state of |0⟩ & |1⟩ with a single gate.</p>", 
    unsafe_allow_html=True
    )
    generic_level(current_level=2)

def level3_page():
    st.title("Level 3: Entanglement")
    st.write("")
    st.markdown(
    "<p style='font-size:24px;'>Create a Bell state: |00⟩ + |11⟩ with two gates.</p>", 
    unsafe_allow_html=True
    )

    generic_level(current_level=3)

def end_page():
    st.title("Congratulations!")
    st.markdown("<h2>You won the VW Quantum Challenge! 🎉</h2>", unsafe_allow_html=True)
    st.markdown("<h2>You are now a quantum expert! 🧠</h2>", unsafe_allow_html=True)
    st.markdown("<h2>You deserve a piece of 🍬🍭</h2>", unsafe_allow_html=True)
    st.image("winner.png")
    add_return_home_button()


# Utility function to add a return to home button
def add_return_home_button():
    if st.button("Return to Home"):
        st.query_params["page"] = "home"
        set_page("home")

def add_tutorial_button():
    if st.button("Tutorial"):
        st.query_params["page"] = "tutorial"
        set_page("tutorial")

def add_explanation_button():
    if st.button("What the heck is Quantum Computing?"):
        st.query_params["page"] = "explanation"
        set_page("explanation")

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
    # Setup for the quantum circuit and simulation
    states = ['0', '1'] if current_level < 3 else ['00', '01', '10', '11']
    simulated_circuit = QuantumCircuit(1) if current_level < 3 else QuantumCircuit(2)

    # Apply gates to the circuit
    for gate in applied_gates:
        if gate == "X":
            simulated_circuit.x(0)
        elif gate == "H":
            simulated_circuit.h(0)
        elif gate == "CNOT":
            simulated_circuit.cx(0, 1)

    # Simulate the circuit
    simulator = AerSimulator(method='statevector')
    simulated_circuit.save_statevector()
    compiled_circuit = transpile(simulated_circuit, simulator)
    sim_result = simulator.run(compiled_circuit).result()
    statevector = sim_result.get_statevector(compiled_circuit)

    # Calculate probabilities
    probabilities = np.abs(statevector)**2

    # Plotting
    fig, ax = plt.subplots()
    ax.bar(range(len(probabilities)), probabilities)
    ax.set_xlabel('State', fontsize=24)
    ax.set_xticks(range(len(probabilities)))
    ax.set_xticklabels([f"|{i}⟩" for i in states], fontsize=30)
    ax.set_ylabel('Probability', fontsize=24)
    ax.set_title('Statevector Probabilities', fontsize=24)
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels([0, 0.5, 1], fontsize=24)

    # Clear the circuit for potential reuse
    simulated_circuit.data.clear()

    return fig

#######################################################
# Main
# Use URL parameters for page navigation
params = st.query_params
page = params.get("page", "home")

# Initialize the session state for page 
if 'page' not in st.session_state:
    st.session_state.page = "home"

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
    st.session_state['page'] = p
    st.rerun()

# Page routing
# if page == "home":
#     home_page()
#     if st.button("Go to Level 1"):
#         set_page("level1")
# elif page == "tutorial":
#     tutorial_page()
#     add_return_home_button()
# elif page == "level1":
#     level1_page()
#     if st.button("Go to Level 2"):
#         set_page("level2")
# elif page == "level2":
#     level2_page()
#     if st.button("Go to Level 3"):
#         set_page("level3")
# elif page == "level3":
#     level3_page()
#     if st.button("Go to End"):
#         set_page("end")
# elif page == "end":
#     end_page()

if st.session_state['page'] == "home":
    home_page()
    if st.button("Go to Level 1"):
        set_page("level1")
elif st.session_state['page'] == "tutorial":
    tutorial_page()
    add_return_home_button()
    add_explanation_button()
elif st.session_state['page'] == "explanation":
    explanation_page()
    add_tutorial_button()
    add_return_home_button()
elif st.session_state['page'] == "level1":
    level1_page()
    if st.button("Go to Level 2"):
        set_page("level2")
elif st.session_state['page'] == "level2":
    level2_page()
    if st.button("Go to Level 3"):
        set_page("level3")
elif st.session_state['page'] == "level3":
    level3_page()
    if st.button("Go to End"):
        set_page("end")
elif st.session_state['page'] == "end":
    end_page()
