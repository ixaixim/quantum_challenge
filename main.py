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
        self.root.title("Quantum Challenge")
        self.current_level = 1
        self.levels_passed = 0  # Step 1: Track levels passed
        self.selected_gate = None
        self.selected_qubit = tk.IntVar(value=0)
        self.state_vector = np.array([[1], [0]])  # Start with |0⟩ state
        self.create_widgets()
        self.reset_challenge()

    def create_widgets(self):
        # Title Label
        self.title_label = tk.Label(self.root, text="Quantum Challenge", font=("Helvetica", 30, "bold"))
        self.title_label.pack(pady=10)

        # Instructions Label
        self.instructions_label = tk.Label(self.root)
        self.instructions_label.pack(pady=10)

        # Levels Passed Label
        self.levels_passed_label = tk.Label(self.root, text=f"Levels Passed: {self.levels_passed}", font=("Helvetica", 16))
        self.levels_passed_label.pack(pady=10)

        # Circuit Canvas
        self.circuit_canvas = tk.Canvas(self.root, width=400, height=100, bg="white")
        self.circuit_canvas.pack(pady=10)
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

        # self.next_button = tk.Button(self.control_buttons_frame, text="Next Level", command=self.next_level)        
        # self.next_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(self.control_buttons_frame, text="Back to Level 1", command=self.go_to_level_1)
        self.back_button.pack(side=tk.LEFT, padx=5)

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
        
        # LaTeX Result Frame
        self.latex_frame = tk.Frame(self.root)
        self.latex_frame.pack(pady=10)
        
        self.latex_figure, self.latex_ax = plt.subplots(figsize=(7, 1))
        self.latex_canvas = FigureCanvasTkAgg(self.latex_figure, master=self.latex_frame)
        self.latex_canvas.get_tk_widget().pack()

        self.update_latex_result(r'|0\rangle')



    def create_gate(self, parent, text):
        button = tk.Button(parent, text=text, bg="blue", fg="white", width=5, command=lambda: self.on_gate_select(text))
        button.pack(side=tk.LEFT, padx=5)

    def on_gate_select(self, text):
        self.selected_gate = text
        self.add_gate_to_circuit(self.selected_gate)
        self.apply_gate(self.selected_gate)

    def reset_challenge(self):
        self.circuit_canvas.delete("all")
        self.gate_items.clear()
        self.state_vector = np.array([[1], [0]]) if self.current_level < 3 else np.array([[1], [0], [0], [0]])  # Reset state
        self.circuit_canvas.create_line(50, 30, 350, 30, width=2)  # Qubit 0 line
        if self.current_level == 3:
            self.circuit_canvas.create_line(50, 70, 350, 70, width=2)  # Qubit 1 line
        self.update_visualizations()
        self.set_instructions()

    def next_level(self):
        self.current_level += 1
        self.levels_passed += 1  # Increment levels passed
        if self.current_level > 3:
            self.current_level = 1
            self.levels_passed = 0  # Reset levels passed at level 1            
        self.reset_challenge()

    def update_levels_passed_display(self):
        # Step 5: Update the display of levels passed
        self.levels_passed_label.config(text=f"Levels Passed: {self.levels_passed}")    

    def go_to_level_1(self):
        self.current_level = 1
        self.levels_passed = 0  # Reset levels passed at level 1
        self.update_levels_passed_display()  # Update the display of levels passed
        self.reset_challenge()

    def apply_gate(self, gate):
        if self.current_level < 3:
            if gate == "X":
                self.apply_x_gate()
            elif gate == "H":
                self.apply_h_gate()
        else:
            if gate == "X":
                self.apply_x_gate_multi(self.selected_qubit.get())
            elif gate == "H":
                self.apply_h_gate_multi(self.selected_qubit.get())
            elif gate == "CNOT":
                self.apply_cnot_gate()

        self.update_qubit_labels()
        self.check_solution()

    def apply_x_gate(self):
        x_gate = np.array([[0, 1], [1, 0]])
        self.state_vector = np.dot(x_gate, self.state_vector)
        self.update_visualizations()

    def apply_h_gate(self):
        h_gate = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        self.state_vector = np.dot(h_gate, self.state_vector)
        self.update_visualizations()

    def apply_x_gate_multi(self, qubit):
        X = np.array([[0, 1], [1, 0]])
        I = np.eye(2)
        if qubit == 0:
            X_I = np.kron(X, I)  # Apply X gate to the first qubit
        else:
            X_I = np.kron(I, X)  # Apply X gate to the second qubit
        self.state_vector = np.dot(X_I, self.state_vector)
        self.update_visualizations()

    def apply_h_gate_multi(self, qubit):
        H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        I = np.eye(2)
        if qubit == 0:
            H_I = np.kron(H, I)  # Apply Hadamard gate to the first qubit
        else:
            H_I = np.kron(I, H)  # Apply Hadamard gate to the second qubit
        self.state_vector = np.dot(H_I, self.state_vector)
        self.update_visualizations()

    def apply_cnot_gate(self):
        CNOT = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1],
                         [0, 0, 1, 0]])
        self.state_vector = np.dot(CNOT, self.state_vector)
        self.update_visualizations()

    def update_qubit_labels(self):
        state_str = self.format_state_vector()
        self.instructions_label.config(text=f"State Vector: {state_str}")

    def set_instructions(self):
        instructions = {
            1: "Level 1: Transform the qubit from",
            2: "Level 2: Create a superposition state.",
            3: "Level 3: Create a Bell state: ",
        }
        self.instructions_label.config(text=instructions[self.current_level])
        # Repack the widget to apply the font size change
        self.instructions_label.pack()

    def check_solution(self):
        solutions = {
            1: np.array([[0], [1]]),  # |1⟩
            2: (1 / np.sqrt(2)) * np.array([[1], [1]]),  # (|0⟩ + |1⟩) / sqrt(2)
            3: (1 / np.sqrt(2)) * np.array([[1], [0], [0], [1]]),  # (|00⟩ + |11⟩) / sqrt(2)
        }
        if np.allclose(self.state_vector, solutions[self.current_level]):
            messagebox.showinfo("Success", "Congratulations! You've completed the level.")
            self.next_level()
            
            self.update_levels_passed_display()  # Update the display of levels passed, if applicable


    def update_visualizations(self):
        if self.current_level < 3:
            bloch_vector = self.state_to_bloch(self.state_vector)
            self.update_bloch_sphere(bloch_vector)
            probabilities = self.state_to_probabilities(self.state_vector)
            self.update_probabilities(probabilities)
            latex_state = self.state_to_latex(self.state_vector)
            self.update_latex_result(latex_state)
        else:
            # For Bell state, clear images and only update the probabilities and LaTeX result
            self.ax.clear()    
            bloch_vector = np.array([[1], [0]]) # placeholder
            self.update_bloch_sphere(bloch_vector)
            probabilities = self.state_to_probabilities(self.state_vector)
            self.update_probabilities_2q(probabilities)

            latex_state = self.state_to_latex(self.state_vector)
            self.update_latex_result(latex_state)

    def state_to_bloch(self, state_vector):
        a, b = state_vector[0, 0], state_vector[1, 0]
        x = 2 * np.real(np.conj(a) * b)
        y = 2 * np.imag(np.conj(a) * b)
        z = np.abs(a)**2 - np.abs(b)**2
        return [x, y, z]

    def state_to_probabilities(self, state_vector):
        return np.abs(state_vector.flatten())**2

    def state_to_latex(self, state_vector):
        state_str = "|ψ⟩ = " + " + ".join(f"{amp} |{idx}⟩" for idx, amp in enumerate(state_vector.flatten()) if amp != 0)
        return state_str

    def format_state_vector(self):
        return ", ".join([f"{amp:.2f}" for amp in self.state_vector.flatten()])

    def update_bloch_sphere(self, vector):
        if self.current_level < 3:
            self.ax.clear()
            self.ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], color='r', arrow_length_ratio=0.1)
            self.ax.set_xlim([-1, 1])
            self.ax.set_ylim([-1, 1])
            self.ax.set_zlim([-1, 1])
            self.ax.set_xlabel('X')
            self.ax.set_ylabel('Y')
            self.ax.set_zlabel('Z')
            self.bloch_canvas.draw()
            self.bloch_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Adjust as per your layout
        else:
            self.ax.cla()
            self.ax.axis('off')
            self.ax.text(0.5, 0.5, 0.5, "Hint: Try using a different gate combination", fontsize=12, ha='center')
            self.bloch_canvas.draw()
            self.bloch_canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Adjust as per your layout


    def update_probabilities(self, probabilities):
        self.prob_ax.clear()
        self.prob_ax.bar(range(len(probabilities)), probabilities)
        self.prob_ax.set_xticks(range(len(probabilities)))
        self.prob_ax.set_xticklabels([f"|{i}⟩" for i in range(len(probabilities))])
        self.prob_ax.set_ylabel('Probability')
        self.prob_canvas.draw()
        

    def update_probabilities_2q(self, probabilities):
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



    def update_latex_result(self, latex_str):
        self.latex_ax.clear()
        self.latex_ax.text(0.1, 0.5, f"${latex_str}$", fontsize=20)
        self.latex_ax.axis('off')
        self.latex_canvas.draw()

    def add_gate_to_circuit(self, gate):
        x = 50 + len(self.gate_items) * 50
        y = 50
        if self.current_level < 3:
            gate_item = self.circuit_canvas.create_rectangle(x, y - 15, x + 30, y + 15, fill="blue", tags="gate")
            text_item = self.circuit_canvas.create_text(x + 15, y, text=gate, fill="white", tags="gate")
            self.gate_items.append((gate_item, text_item))
        else:
            qubit = self.selected_qubit.get()
            y = 30 if qubit == 0 else 70
            gate_item = self.circuit_canvas.create_rectangle(x, y - 10, x + 20, y + 10, fill="blue", tags="gate")
            text_item = self.circuit_canvas.create_text(x + 10, y, text=gate, fill="white", tags="gate")
            self.gate_items.append((gate_item, text_item))
            if gate == "CNOT":
                self.circuit_canvas.create_line(x + 10, 30, x + 10, 70, width=2, tags="gate")
                self.circuit_canvas.create_oval(x + 7, 67, x + 13, 73, fill="blue", tags="gate")

    def on_gate_button_click(self):
        if self.selected_gate is not None:
            self.add_gate_to_circuit(self.selected_gate)
            self.apply_gate(self.selected_gate)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumChallengeApp(root)
    root.mainloop()
