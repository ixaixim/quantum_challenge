import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Set up virtual display if not available
if os.environ.get('DISPLAY', '') == '':
    print('No display found. Using Xvfb.')
    os.system('Xvfb :99 -ac &')
    os.environ['DISPLAY'] = ':99'

class QuantumChallengeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Challenge")
        self.current_level = 1
        self.selected_gate = None
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
        self.circuit_canvas = tk.Canvas(self.root, width=400, height=100, bg="white")
        self.circuit_canvas.pack(pady=10)
        self.circuit_canvas.create_line(50, 50, 350, 50, width=2)  # Qubit line
        self.circuit_canvas.bind("<Button-1>", self.on_circuit_click)
        self.gate_items = []

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

        self.update_bloch_sphere([0, 0, 1])

        # Probability Distribution Visualization
        self.probability_frame = tk.Frame(self.visualization_frame)
        self.probability_frame.pack(side=tk.LEFT, padx=10)

        self.prob_figure, self.prob_ax = plt.subplots()
        self.prob_canvas = FigureCanvasTkAgg(self.prob_figure, master=self.probability_frame)
        self.prob_canvas.get_tk_widget().pack()

        self.update_probabilities([1, 0])

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
            self.apply_gate(self.selected_gate)
            self.selected_gate = None

    def reset_challenge(self):
        self.qubits = ["|0⟩"]
        self.update_qubit_labels()
        self.set_instructions()
        self.update_bloch_sphere([0, 0, 1])
        self.update_probabilities([1, 0])
        self.circuit_canvas.delete("gate")
        self.gate_items.clear()

    def next_level(self):
        self.current_level += 1
        if (self.current_level > 3):
            messagebox.showinfo("Congratulations!", "You've completed all levels!")
            self.current_level = 1
        self.reset_challenge()

    def apply_gate(self, gate):
        if gate == "X":
            self.qubits[0] = "|1⟩" if self.qubits[0] == "|0⟩" else "|0⟩"
            self.update_bloch_sphere([0, 0, -1] if self.qubits[0] == "|1⟩" else [0, 0, 1])
            self.update_probabilities([0, 1] if self.qubits[0] == "|1⟩" else [1, 0])
        elif gate == "H":
            self.qubits[0] = "superposition"
            self.update_bloch_sphere([1, 0, 0])
            self.update_probabilities([0.5, 0.5])
        elif gate == "CNOT":
            # Assuming this is the first qubit, you can expand this to multiple qubits later
            if self.qubits[0] == "superposition":
                self.qubits[0] = "entangled"
                self.update_probabilities([0.5, 0.5])  # This is a simplification
        self.update_qubit_labels()
        self.check_solution()

    def update_qubit_labels(self):
        self.instructions_label.config(text=f"Qubit: {self.qubits[0]}")

    def set_instructions(self):
        instructions = {
            1: "Level 1: Transform the qubit from |0⟩ to |1⟩ using the X gate.",
            2: "Level 2: Create a superposition state using the H gate.",
            3: "Level 3: Entangle two qubits to create the Bell state using the H and CNOT gates."
        }
        self.instructions_label.config(text=instructions[self.current_level])

    def check_solution(self):
        solutions = {
            1: ["|1⟩"],
            2: ["superposition"],
            3: ["entangled"]  # Simplification for single qubit
        }
        if self.qubits == solutions[self.current_level]:
            messagebox.showinfo("Success!", f"You've completed Level {self.current_level}!")

    def update_bloch_sphere(self, vector):
        self.ax.cla()
        self.ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], color='b')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Bloch Sphere')
        self.bloch_canvas.draw()

    def update_probabilities(self, probabilities):
        self.prob_ax.cla()
        self.prob_ax.bar([0, 1], probabilities, color='b')
        self.prob_ax.set_ylim(0, 1)
        self.prob_ax.set_xticks([0, 1])
        self.prob_ax.set_xticklabels(['0', '1'])
        self.prob_ax.set_xlabel('State')
        self.prob_ax.set_ylabel('Probability')
        self.prob_ax.set_title('Probabilities')
        self.prob_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumChallengeApp(root)
    root.mainloop()
