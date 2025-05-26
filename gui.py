import tkinter as tk
from tkinter import ttk, messagebox
from solvers import solve_n_queens_backtracking, solve_n_queens_genetic

class NQueensGUI:
    def __init__(self, master):
        self.master = master
        master.title("N-Queens Solver")
        master.geometry("600x750")

        self.n_value = tk.IntVar(value=8)
        self.algorithm_var = tk.StringVar(value="Backtracking") # مقدار پیش‌فرض

        control_frame = ttk.Frame(master, padding="10")
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="N:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.n_entry = ttk.Entry(control_frame, textvariable=self.n_value, width=5)
        self.n_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(control_frame, text="Algorithm:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        algorithms = ["Backtracking", "Genetic Algorithm"]
        self.algo_combo = ttk.Combobox(control_frame, textvariable=self.algorithm_var, values=algorithms, state="readonly", width=20)
        self.algo_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        if algorithms: # اطمینان از اینکه لیست خالی نیست
            self.algo_combo.current(0)


        self.solve_button = ttk.Button(control_frame, text="Solve", command=self.solve_clicked)
        self.solve_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        
        control_frame.columnconfigure(1, weight=1)

        self.board_frame = ttk.Frame(master, relief="sunken", borderwidth=2)
        self.board_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.canvas = tk.Canvas(self.board_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.info_frame = ttk.Frame(master, padding="5")
        self.info_frame.pack(pady=5, fill="x")
        
        self.status_label = ttk.Label(self.info_frame, text="Enter N and select an algorithm.", wraplength=580)
        self.status_label.pack(pady=2, fill="x")
        self.solution_text_label = ttk.Label(self.info_frame, text="Solution: N/A", wraplength=580)
        self.solution_text_label.pack(pady=2, fill="x")
        self.time_label = ttk.Label(self.info_frame, text="Time: N/A", wraplength=580)
        self.time_label.pack(pady=2, fill="x")
        self.num_solutions_label = ttk.Label(self.info_frame, text="Total solutions (for exact solvers): N/A", wraplength=580)
        self.num_solutions_label.pack(pady=2, fill="x")

        self.current_solution = None
        self.current_n = 0

    def on_canvas_resize(self, event):
        if self.current_solution:
            self.draw_board(self.current_solution, self.current_n)
        elif self.current_n > 0:
            self.draw_empty_board(self.current_n)

    def draw_board(self, solution, n):
        self.canvas.delete("all")
        self.current_solution = solution
        self.current_n = n
        
        if n == 0: return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        cell_size = min(canvas_width / n, canvas_height / n)
        if cell_size < 1: return

        offset_x = (canvas_width - cell_size * n) / 2
        offset_y = (canvas_height - cell_size * n) / 2

        for row in range(n):
            for col in range(n):
                x1, y1 = offset_x + col * cell_size, offset_y + row * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = "white" if (row + col) % 2 == 0 else "lightgray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                if solution and solution[row] == col:
                    queen_char_size = int(cell_size * 0.6)
                    if queen_char_size < 1 : queen_char_size = 1
                    self.canvas.create_text(x1 + cell_size / 2, y1 + cell_size / 2,
                                            text="♛", font=("Arial", queen_char_size), fill="black")
        self.master.update_idletasks()

    def draw_empty_board(self, n):
        self.draw_board(None, n)

    def solve_clicked(self):
        try:
            n = self.n_value.get()
            if n <= 0:
                messagebox.showerror("Error", "N must be a positive integer.")
                return
            if n > 20 and self.algorithm_var.get() == "Backtracking":
                 if not messagebox.askyesno("Warning", f"N={n} might take a very long time for Backtracking. Continue?"):
                    return
            if n > 30 and self.algorithm_var.get() == "Genetic Algorithm":
                 if not messagebox.askyesno("Warning", f"N={n} for Genetic Algorithm might take a while. Continue?"):
                    return

            self.status_label.config(text=f"Solving for N={n} using {self.algorithm_var.get()}...")
            self.solution_text_label.config(text="Solution: N/A")
            self.time_label.config(text="Time: N/A")
            self.num_solutions_label.config(text="Total solutions: N/A")
            self.current_solution = None
            self.current_n = n
            self.draw_empty_board(n)
            self.master.update_idletasks()

            algo = self.algorithm_var.get()
            solution, elapsed_time, num_sols = None, 0, 0

            if algo == "Backtracking":
                solution, elapsed_time, num_sols = solve_n_queens_backtracking(n)
            # بلوک CSP حذف شد
            elif algo == "Genetic Algorithm":
                pop_size, generations = 100, 500
                if n < 4:
                    messagebox.showinfo("Info", "Genetic Algorithm is less suitable for N < 4. Backtracking is preferred.")
                    if n == 1: solution, elapsed_time, num_sols = [0], 0.0, 1
                    else: solution, elapsed_time, num_sols = None, 0.0, 0
                else:
                    if n > 15 : generations = 1000
                    if n > 25 : generations = 1500
                    if n > 10 : pop_size = max(100, n * 5)
                    solution, elapsed_time, num_sols = solve_n_queens_genetic(n, population_size=pop_size, generations=generations)
            
            if solution:
                self.status_label.config(text=f"Solution found for N={n} using {self.algorithm_var.get()}.")
                self.solution_text_label.config(text=f"Solution: {solution}")
                self.draw_board(solution, n)
            else:
                self.status_label.config(text=f"No solution found for N={n} with {self.algorithm_var.get()}.")
                self.solution_text_label.config(text="Solution: None")
                self.draw_empty_board(n)
            
            self.time_label.config(text=f"Time: {elapsed_time:.4f} seconds")
            if algo == "Backtracking": 
                self.num_solutions_label.config(text=f"Total unique solutions found by solver: {num_sols}")
            elif algo == "Genetic Algorithm":
                 self.num_solutions_label.config(text=f"Perfect solution found by GA: {'Yes' if num_sols > 0 else 'No'}")

        except ValueError:
            messagebox.showerror("Error", "N must be an integer.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            print(f"Error: {e}")