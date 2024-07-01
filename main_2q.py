import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

# Set up virtual display if not available
if os.environ.get('DISPLAY', '') == '':
    print('No display found. Using Xvfb.')
    os.system('Xvfb :99 -ac &')
    os.environ['DISPLAY'] = ':99'

class QuantumChallengeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Challenge - Bell State")
        self.current_level = 3
        self.state_vector = np.array([[1], [0], [0], [0]])  # Start with |00⟩ state
        self.selected_qubit = tk.IntVar(value=0)
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="Quantum Challenge - Bell State", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Instructions Label
        self.instructions_label = tk.Label(self.root, text="Creating Bell State: |00⟩ + |11⟩", wraplength=400, font=("Helvetica", 12))
        self.instructions_label.pack(pady=10)

        # Circuit Canvas
        self.circuit_canvas = tk.Canvas(self.root, width=400, height=100, bg="white")
        self.circuit_canvas.pack(pady=10)
        self.circuit_canvas.create_line(50, 30, 350, 30, width=2)  # Qubit 0 line
        self.circuit_canvas.create_line(50, 70, 350, 70, width=2)  # Qubit 1 line

        # Qubit Selection
        self.qubit_selection_frame = tk.Frame(self.root)
        self.qubit_selection_frame.pack(pady=10)
        tk.Radiobutton(self.qubit_selection_frame, text="Qubit 0", variable=self.selected_qubit, value=0).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.qubit_selection_frame, text="Qubit 1", variable=self.selected_qubit, value=1).pack(side=tk.LEFT, padx=5)

        # Gate Palette
        self.gate_palette = tk.Frame(self.root)
        self.gate_palette.pack(pady=10)

        self.create_gate(self.gate_palette, "X")
        self.create_gate(self.gate_palette, "H")
        self.create_gate(self.gate_palette, "CNOT")

        # Control Buttons
        self.control_buttons_frame = tk.Frame(self.root)
        self.control_buttons_frame.pack(pady=10)

        self.reset_button = tk.Button(self.control_buttons_frame, text="Reset", command=self.reset_challenge)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # LaTeX Result Display
        self.latex_frame = tk.Frame(self.root)
        self.latex_frame.pack(pady=10)
        self.latex_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(4, 2)), master=self.latex_frame)
        self.latex_canvas.get_tk_widget().pack()
        self.latex_ax = self.latex_canvas.figure.subplots()

        # Probabilities Display
        self.prob_frame = tk.Frame(self.root)
        self.prob_frame.pack(pady=10)
        self.prob_canvas = FigureCanvasTkAgg(plt.Figure(figsize=(4, 2)), master=self.prob_frame)
        self.prob_canvas.get_tk_widget().pack()
        self.prob_ax = self.prob_canvas.figure.subplots()

    def create_gate(self, parent, gate_type):
        button = tk.Button(parent, text=gate_type, command=lambda: self.add_gate(gate_type))
        button.pack(side=tk.LEFT, padx=5)

    def reset_challenge(self):
        self.state_vector = np.array([[1], [0], [0], [0]])  # Reset to |00⟩ state
        self.update_display()

    def add_gate(self, gate_type):
        if gate_type == "X":
            self.apply_x_gate(self.selected_qubit.get())
        elif gate_type == "H":
            self.apply_hadamard_gate(self.selected_qubit.get())
        elif gate_type == "CNOT":
            self.apply_cnot_gate()
        self.update_display()

    def apply_x_gate(self, qubit):
        X = np.array([[0, 1], [1, 0]])
        I = np.eye(2)
        if qubit == 0:
            X_I = np.kron(X, I)  # Apply X gate to the first qubit
        else:
            X_I = np.kron(I, X)  # Apply X gate to the second qubit
        self.state_vector = np.dot(X_I, self.state_vector)

    def apply_hadamard_gate(self, qubit):
        H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        I = np.eye(2)
        if qubit == 0:
            H_I = np.kron(H, I)  # Apply Hadamard gate to the first qubit
        else:
            H_I = np.kron(I, H)  # Apply Hadamard gate to the second qubit
        self.state_vector = np.dot(H_I, self.state_vector)

    def apply_cnot_gate(self):
        CNOT = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0]])
        self.state_vector = np.dot(CNOT, self.state_vector)

    def update_display(self):
        state_str = self.format_state_vector()
        self.update_latex_result(state_str)
        self.update_probabilities()

    def format_state_vector(self):
        coefficients = self.state_vector.flatten()
        state_str = f'{coefficients[0]:.2f}|00⟩ + {coefficients[1]:.2f}|01⟩ + {coefficients[2]:.2f}|10⟩ + {coefficients[3]:.2f}|11⟩'
        return state_str

    def update_latex_result(self, latex_str):
        self.latex_ax.cla()
        self.latex_ax.text(0.5, 0.5, f'${latex_str}$', horizontalalignment='center', verticalalignment='center', fontsize=20)
        self.latex_ax.axis('off')
        self.latex_canvas.draw()

    def update_probabilities(self):
        probabilities = np.abs(self.state_vector)**2
        self.prob_ax.cla()
        self.prob_ax.bar([0, 1, 2, 3], probabilities.flatten(), color='b')
        self.prob_ax.set_ylim(0, 1)
        self.prob_ax.set_xticks([0, 1, 2, 3])
        self.prob_ax.set_xticklabels(['00', '01', '10', '11'])
        self.prob_ax.set_xlabel('State')
        self.prob_ax.set_ylabel('Probability')
        self.prob_ax.set_title('Probabilities')
        self.prob_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumChallengeApp(root)
    root.mainloop()
