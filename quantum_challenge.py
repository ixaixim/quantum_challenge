import streamlit as st
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

# Define the main application class
class QuantumChallengeApp:
    def __init__(self):
        """
        Initialize the Quantum Challenge application with predefined levels and instructions.
        """
        self.instructions = {
            1: "Level 1: Transform the qubit from |0⟩ to |1⟩ with a single gate.",
            2: "Level 2: Create a superposition state of |0⟩ & |1⟩ with a single gate.",
            3: "Level 3: Create a Bell state: |00⟩ + |11⟩ with two gates.",
        }
        self.current_level = 1
        self.selected_gate = "X"
        self.applied_gates = []  # List to track applied gates
        self.circuit = QuantumCircuit(1)
        self.states = ['0', '1'] if self.current_level < 3 else ['00', '01', '10', '11']

    def apply_gate(self, gate):
        """
        Apply a selected gate to the quantum circuit.
        
        Parameters:
        gate (str): The gate to be applied ('X', 'H', 'CNOT').
        """
        if not hasattr(self, 'circuit') or self.circuit is None:
            self.init_circuit()
        
        if gate == "X":
            if self.current_level < 3:
                self.circuit.x(0)
            else:
                self.circuit.x(self.selected_qubit)
        elif gate == "H":
            if self.current_level < 3:
                self.circuit.h(0)
            else:
                self.circuit.h(self.selected_qubit)
        elif gate == "CNOT" and self.current_level >= 3:
            self.circuit.cx(0, 1)
        
        self.applied_gates.append(gate)

    def init_circuit(self):
        """
        Initialize the quantum circuit based on the current level.
        """
        if self.current_level < 3:
            self.circuit = QuantumCircuit(1)
        else:
            self.circuit = QuantumCircuit(2)
        self.state_vector = [1, 0] if self.current_level < 3 else [1, 0, 0, 0]
        self.states = ['0', '1'] if self.current_level < 3 else ['00', '01', '10', '11']
        self.selected_qubit = 0

    def reset_circuit(self):
        """
        Reset the quantum circuit to its initial state.
        """
        self.init_circuit()
        self.applied_gates = []

    def refresh_game(self):
        """
        Reset the game to level 1.
        """
        self.current_level = 1
        self.init_circuit()
        
    def next_level(self):
        """
        Proceed to the next level in the game.
        
        Returns:
        bool: True if the last level is completed, otherwise False.
        """
        self.current_level += 1
        if self.current_level > 3:
            return True
        else:
            self.reset_circuit()
            return False

    def check_solution(self):
        """
        Check if the applied gates result in the correct quantum state for the current level.
        
        Returns:
        bool: True if the solution is correct, otherwise False.
        """
        print("checking results... please wait")
        self.circuit.save_statevector()
        simulated_circuit = self.circuit
        for gate in self.applied_gates:
            if self.current_level < 3:
                if gate == "X":
                    simulated_circuit.x(0)
                elif gate == "H":
                    simulated_circuit.h(0)
            else:
                if gate == "X":
                    simulated_circuit.x(self.selected_qubit)
                elif gate == "H":
                    simulated_circuit.h(self.selected_qubit)
                elif gate == "CNOT":
                    simulated_circuit.cx(0, 1)

        simulator = AerSimulator(method='statevector')
        compiled_circuit = transpile(self.circuit, simulator)
        sim_result = simulator.run(compiled_circuit).result()
        statevector = sim_result.get_statevector(compiled_circuit)

        solutions = {
            1: np.array([0, 1]),  # |1⟩
            2: np.array([1/np.sqrt(2), 1/np.sqrt(2)]),  # (|0⟩ + |1⟩) / sqrt(2)
            3: np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]),  # (|00⟩ + |11⟩) / sqrt(2)
        }

        target_state = solutions[self.current_level]
        statevector_np = np.array(statevector)

        target_probabilities = np.abs(target_state) ** 2
        state_probabilities = np.abs(statevector_np) ** 2
        self.circuit.data.clear()

        return np.allclose(state_probabilities, target_probabilities, atol=1e-2)

    def draw_circuit(self):
        """
        Draw the quantum circuit with the applied gates.
        
        Returns:
        matplotlib.figure.Figure: The figure of the drawn quantum circuit.
        """
        print("inside draw circuit")
        print(self.applied_gates)
        simulated_circuit = self.circuit
        for gate in self.applied_gates:
            if self.current_level < 3:
                if gate == "X":
                    simulated_circuit.x(0)
                elif gate == "H":
                    simulated_circuit.h(0)
            else:
                if gate == "X":
                    simulated_circuit.x(self.selected_qubit)
                elif gate == "H":
                    simulated_circuit.h(self.selected_qubit)
                elif gate == "CNOT":
                    simulated_circuit.cx(0, 1)
        return circuit_drawer(simulated_circuit, output='mpl')

    def plot_statevector(self):
        """
        Plot the statevector probabilities of the quantum circuit.
        
        Returns:
        matplotlib.figure.Figure: The figure of the statevector probabilities.
        """
        print("About to plot")
        self.init_circuit()
        print("see self.circuit above")
        print()
        simulated_circuit = self.circuit
        for gate in self.applied_gates:
            if self.current_level < 3:
                if gate == "X":
                    simulated_circuit.x(0)
                elif gate == "H":
                    simulated_circuit.h(0)
            else:
                if gate == "X":
                    simulated_circuit.x(self.selected_qubit)
                elif gate == "H":
                    simulated_circuit.h(self.selected_qubit)
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
        ax.set_xticklabels([f"|{i}⟩" for i in self.states])
        ax.set_ylabel('Probability')
        ax.set_title('Statevector Probabilities')
        print()
        self.circuit.data.clear()
        print("circuit after clearing")
        return fig

def main():
    """
    The main function to run the Streamlit application.
    """
    st.markdown(
        """
        <h1 style='text-align: center;'>Quantum Challenge</h1>
        """,
        unsafe_allow_html=True
    )
    if "app_instance" not in st.session_state:
        st.session_state.app_instance = QuantumChallengeApp()
    app = st.session_state.app_instance

    header_placeholder = st.empty()  # Placeholder for the header
    header_placeholder.markdown(
        f"<h3 style='font-weight: bold;'>{app.instructions[app.current_level]}</h3>",
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    gate = st.selectbox('Select Gate', ['X', 'H', 'CNOT'] if app.current_level == 3 else ['X', 'H'])

    if st.button('Apply Gate'):
        app.apply_gate(gate)
        cols[1].pyplot(app.plot_statevector())
        cols[0].pyplot(app.draw_circuit())
        
    if app.check_solution():
        st.success("Congratulations! You've completed the level. Play the Next Level")
        if app.next_level():
            st.info("You are an Advanced Quantum user! You have Reached the end of the game!!")
            cols[0].empty()
            cols[1].empty()
            st.image("winner.png")
    else:
        st.error("The solution is not correct. Please try again.")        

    if st.button('Reset'):
        app.reset_circuit()
        cols[0].pyplot(app.draw_circuit())
        cols[1].pyplot(app.plot_statevector())

    if st.button("Refresh Game"):
        app.refresh_game()

    if st.session_state.get('first_plot', True):
        cols[0].pyplot(app.draw_circuit())
        cols[1].pyplot(app.plot_statevector())
        st.session_state.first_plot = False

main()
