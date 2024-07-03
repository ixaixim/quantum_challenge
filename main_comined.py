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
        self.root.geometry("1220x1080")  # Width x Height
        self.root.title("Quantum Challenge")
        self.current_level = 1
        self.selected_gate = None
        self.selected_qubit = tk.IntVar(value=0)
        self.state_vector = None
        self.create_widgets()
        self.reset_challenge()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="Quantum Challenge", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Instructions Label
        self.instructions_label = tk.Label(self.root, text="", wraplength=400, font=("Helvetica", 12))
        self.instructions_label.pack(pady=10)

        # Circuit Canvas
        self.circuit_canvas = tk.Canvas(self.root, width=500, height=150, bg="white")
        self.circuit_canvas.pack(pady=10)
        self.circuit_canvas.bind("<Button-1>", self.on_circuit_click)

        # Qubit Selection
        self.qubit_selection_frame = tk.Frame(self.root)
        self.qubit_selection_frame.pack(pady=10)

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

        self.next_button = tk.Button(self.control_buttons_frame, text="Next Level", command=self.next_level)
        self.next_button.pack(side=tk.LEFT, padx=5)

        # Visualization Frames
        self.visualization_frame = tk.Frame(self.root)
        self.visualization_frame.pack(pady=10)

        # Bloch Sphere Visualization
        self.bloch_sphere_frame = tk.Frame(self.visualization_frame)
        self.bloch_sphere_frame.pack(side=tk.LEFT, padx=10)

        self.figure, self.ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.bloch_canvas = FigureCanvasTkAgg(self.figure, master=self.bloch_sphere_frame)
        self.bloch_canvas.get_tk_widget().pack()

        # Probability Distribution Visualization
        self.probability_frame = tk.Frame(self.visualization_frame)
        self.probability_frame.pack(side=tk.LEFT, padx=10)

        self.prob_figure, self.prob_ax = plt.subplots()
        self.prob_canvas = FigureCanvasTkAgg(self.prob_figure, master=self.probability_frame)
        self.prob_canvas.get_tk_widget().pack()

        # LaTeX Result Display
        self.latex_frame = tk.Frame(self.root)
        self.latex_frame.pack(pady=10)
        
        self.latex_figure, self.latex_ax = plt.subplots()
        self.latex_canvas = FigureCanvasTkAgg(self.latex_figure, master=self.latex_frame)
        self.latex_canvas.get_tk_widget().pack()

    def create_gate(self, parent, text):
        button = tk.Button(parent, text=text, bg="blue", fg="white", width=5, command=lambda: self.on_gate_select(text))
        button.pack(side=tk.LEFT, padx=5)

    def on_gate_select(self, text):
        self.selected_gate = text

    def on_circuit_click(self, event):
        if self.selected_gate is not None:
            x = event.x
            y = event.y
            self.circuit_canvas.create_text(x, y, text=self.selected_gate, tags="gate", fill="blue")
            if self.current_level == 3:
                self.apply_gate_level3(self.selected_gate)
            else:
                self.apply_gate(self.selected_gate)
            self.selected_gate = None

    def reset_challenge(self):
        self.circuit_canvas.delete("gate")
        if self.current_level == 3:
            self.state_vector = np.array([[1], [0], [0], [0]])  # Reset to |00⟩ state
            self.circuit_canvas.create_line(50, 30, 350, 30, width=2)  # Qubit 0 line
            self.circuit_canvas.create_line(50, 70, 350, 70, width=2)  # Qubit 1 line
        else:
            self.state_vector = np.array([[1], [0]])  # Reset to |0⟩ state
            self.circuit_canvas.create_line(50, 50, 350, 50, width=2)  # Qubit line
        self.set_instructions()
        self.update_display()

    def next_level(self):
        self.current_level += 1
        if self.current_level > 3:
            self.current_level = 1
        self.reset_challenge()

    def apply_gate(self, gate):
        if gate == "X":
            self.apply_x_gate()
        elif gate == "H":
            self.apply_h_gate()
        self.update_display()
        self.check_solution()

    def apply_gate_level3(self, gate):
        if gate == "X":
            self.apply_x_gate(self.selected_qubit.get())
        elif gate == "H":
            self.apply_h_gate(self.selected_qubit.get())
        elif gate == "CNOT":
            self.apply_cnot_gate()
        self.update_display()

    def apply_x_gate(self, qubit=0):
        X = np.array([[0, 1], [1, 0]])
        I = np.eye(2)
        if self.current_level == 3:
            if qubit == 0:
                X_I = np.kron(X, I)  # Apply X gate to the first qubit
            else:
                X_I = np.kron(I, X)  # Apply X gate to the second qubit
            self.state_vector = np.dot(X_I, self.state_vector)
        else:
            self.state_vector = np.dot(X, self.state_vector)

    def apply_h_gate(self, qubit=0):
        H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        I = np.eye(2)
        if self.current_level == 3:
            if qubit == 0:
                H_I = np.kron(H, I)  # Apply Hadamard gate to the first qubit
            else:
                H_I = np.kron(I, H)  # Apply Hadamard gate to the second qubit
            self.state_vector = np.dot(H_I, self.state_vector)
        else:
            self.state_vector = np.dot(H, self.state_vector)

    def apply_cnot_gate(self):
        CNOT = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0]])
        self.state_vector = np.dot(CNOT, self.state_vector)

    def update_display(self):
        if self.current_level == 3:
            state_str = self.format_state_vector()
            self.update_latex_result(state_str)
            self.update_probabilities()
        else:
            bloch_vector = self.state_to_bloch_vector()
            self.update_bloch_sphere(bloch_vector)
            probabilities = self.state_to_probabilities()
            self.update_probabilities(probabilities)
            state_str = self.format_state_vector()
            self.update_latex_result(state_str)

    def format_state_vector(self):
        coefficients = self.state_vector.flatten()
        if self.current_level == 3:
            state_str = f'{coefficients[0]:.2f}|00⟩ + {coefficients[1]:.2f}|01⟩ + {coefficients[2]:.2f}|10⟩ + {coefficients[3]:.2f}|11⟩'
        else:
            alpha = coefficients[0]
            beta = coefficients[1]
            state_str = f'{alpha:.2f}|0⟩ + {beta:.2f}|1⟩'
        return state_str

    def update_latex_result(self, latex_str):
        self.latex_ax.cla()
        self.latex_ax.text(0.5, 0.5, f'${latex_str}$', horizontalalignment='center', verticalalignment='center', fontsize=20)
        self.latex_ax.axis('off')
        self.latex_canvas.draw()

    def update_probabilities(self, probabilities=None):
        if self.current_level == 3:
            probabilities = np.abs(self.state_vector)**2
            self.prob_ax.cla()
            self.prob_ax.bar([0, 1, 2, 3], probabilities.flatten(), tick_label=['|00⟩', '|01⟩', '|10⟩', '|11⟩'])
            self.prob_ax.set_ylim([0, 1])
            self.prob_ax.set_ylabel('Probability')
            self.prob_ax.set_title('Probability Distribution')
            self.prob_canvas.draw()
        else:
            self.prob_ax.cla()
            self.prob_ax.bar([0, 1], probabilities, tick_label=['|0⟩', '|1⟩'])
            self.prob_ax.set_ylim([0, 1])
            self.prob_ax.set_ylabel('Probability')
            self.prob_ax.set_title('Probability Distribution')
            self.prob_canvas.draw()

    def update_bloch_sphere(self, bloch_vector):
        self.ax.cla()
        u, v = np.mgrid[0:2 * np.pi:100j, 0:np.pi:50j]
        x = np.cos(u) * np.sin(v)
        y = np.sin(u) * np.sin(v)
        z = np.cos(v)
        self.ax.plot_wireframe(x, y, z, color="r", alpha=0.1)

        self.ax.quiver(0, 0, 0, bloch_vector[0], bloch_vector[1], bloch_vector[2], color='b')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Bloch Sphere')
        self.bloch_canvas.draw()

    def state_to_bloch_vector(self):
        alpha = self.state_vector[0, 0]
        beta = self.state_vector[1, 0]
        x = 2 * np.real(np.conj(alpha) * beta)
        y = 2 * np.imag(np.conj(alpha) * beta)
        z = np.abs(alpha)**2 - np.abs(beta)**2
        return np.array([x, y, z])

    def state_to_probabilities(self):
        probabilities = np.abs(self.state_vector)**2
        return probabilities.flatten()

    def check_solution(self):
        target_state = np.array([[1], [1]]) / np.sqrt(2)
        if np.allclose(self.state_vector, target_state, atol=0.1):
            messagebox.showinfo("Congratulations!", "You've reached the target state!")

    def set_instructions(self):
        if self.current_level == 1:
            self.instructions_label.config(text="Level 1: Apply a sequence of gates to transform the state from |0⟩ to |+⟩.")
        elif self.current_level == 2:
            self.instructions_label.config(text="Level 2: Apply a sequence of gates to transform the state from |0⟩ to |1⟩.")
        elif self.current_level == 3:
            self.instructions_label.config(text="Level 3: Apply a sequence of gates to entangle the qubits in a Bell state.")


if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumChallengeApp(root)
    root.mainloop()
