import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import sympy
from sympy import symbols, limit, diff, integrate, solve, Function, dsolve, Eq, sin, cos, tan, exp, log, sqrt

#+++++++++++++++ Color Scheme +++++++++++++++++++
backgroundColour = '#282c34'
foregroundColour = '#c6c6c6'
accentColour = '#61afef'
buttonBg = '#3c424a'
buttonHover = '#4a5260'

#+++++++++++++++ MAT1512 Solver Window +++++++++++++++++++
class MAT1512Window(tk.Toplevel):
    def __init__(self, parent, topicName):
        super().__init__(parent)
        
        self.title(f"MAT1512 - {topicName}")
        self.geometry("950x750")
        self.configure(bg=backgroundColour)
        
        # Disable parent interaction
        parent.attributes('-disabled', True)
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close(parent))
        
        self.topicName = topicName
        self.entries = {} 
        
        self.createInterface()

    def createInterface(self):
        # --- Header ---
        headerFrame = tk.Frame(self, bg=backgroundColour)
        headerFrame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            headerFrame,
            text=f"📈 {self.topicName}",
            font=("Arial", 18, "bold"),
            bg=backgroundColour,
            fg=accentColour
        ).pack()
        
        tk.Label(
            headerFrame,
            text="Enter function and parameters for Step-by-Step Calculus Solutions",
            font=("Arial", 10),
            bg=backgroundColour,
            fg=foregroundColour
        ).pack(pady=(5, 0))

        # --- Main Layout ---
        contentFrame = tk.Frame(self, bg=backgroundColour)
        contentFrame.pack(fill="both", expand=True, padx=20, pady=10)

        # 1. LEFT SIDE: Inputs
        leftPanel = tk.Frame(contentFrame, bg=backgroundColour, width=320)
        leftPanel.pack(side="left", fill="y", padx=(0, 20), anchor="n")

        # Task Selector
        tk.Label(
            leftPanel, 
            text="Select Task:", 
            bg=backgroundColour, 
            fg=foregroundColour,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.taskVar = tk.StringVar()
        tasks = self.getTasks()
        self.taskVar.set(tasks[0])
        
        dropdown = ttk.Combobox(leftPanel, textvariable=self.taskVar, values=tasks, state="readonly", width=35)
        dropdown.pack(fill="x", pady=(0, 15))
        dropdown.bind("<<ComboboxSelected>>", self.updateInputFields)

        # Input Fields Container
        self.inputFrame = tk.LabelFrame(
            leftPanel, 
            text="Input Data", 
            bg=backgroundColour, 
            fg=accentColour, 
            font=("Arial", 10, "bold"),
            padx=10, pady=10
        )
        self.inputFrame.pack(fill="x", pady=5)
        
        # Initialize inputs
        self.updateInputFields()

        # Calculate Button
        solveButton = tk.Button(
            leftPanel,
            text="📝 Solve Step-by-Step",
            command=self.solve_step_by_step,
            bg=accentColour,
            fg='white',
            font=("Arial", 11, "bold"),
            relief='flat',
            cursor='hand2',
            pady=10
        )
        solveButton.pack(fill="x", pady=20)

        # Clear Button
        clearButton = tk.Button(
            leftPanel,
            text="🗑️ Clear",
            command=self.clearInputs,
            bg=buttonBg,
            fg=foregroundColour,
            font=("Arial", 10),
            relief='flat',
            cursor='hand2'
        )
        clearButton.pack(fill="x")

        # 2. RIGHT SIDE: Solution Display
        rightPanel = tk.Frame(contentFrame, bg=backgroundColour)
        rightPanel.pack(side="right", fill="both", expand=True)

        tk.Label(
            rightPanel, 
            text="Mathematical Solution:", 
            bg=backgroundColour, 
            fg=foregroundColour,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.solutionText = scrolledtext.ScrolledText(
            rightPanel,
            font=("Courier", 11),
            bg='#1e1e1e',
            fg=foregroundColour,
            wrap="word",
            padx=15, pady=15
        )
        self.solutionText.pack(fill="both", expand=True, pady=5)
        
        # Back Button
        tk.Button(
            self,
            text="← Back to Topics",
            command=lambda: self.on_close(self.master),
            bg=backgroundColour,
            fg=accentColour,
            font=("Arial", 10),
            relief='flat',
            cursor='hand2',
            pady=10
        ).pack(side="bottom", pady=10)

    def getTasks(self):
        # Return tasks based on the Topic Name (Chapters)
        if "Limits" in self.topicName:
            return ["Limit as x->a", "Limit at Infinity", "Left/Right Hand Limits"]
        elif "Differentiation" in self.topicName:
            return ["Find Derivative f'(x)", "Implicit Differentiation", "Equation of Tangent Line", "Higher Order Derivative"]
        elif "Integrals" in self.topicName:
            return ["Indefinite Integral", "Definite Integral", "Area Under Curve"]
        elif "Differential Equations" in self.topicName:
            return ["Separable First-Order DE", "Exponential Growth/Decay"]
        elif "Partial" in self.topicName:
            return ["Partial Derivative fx", "Partial Derivative fy", "Second Order Partials"]
        else:
            return ["Standard Calculation"]

    def updateInputFields(self, event=None):
        for widget in self.inputFrame.winfo_children():
            widget.destroy()
        self.entries = {}
        
        task = self.taskVar.get()
        fields = []
        
        # --- LIMITS ---
        if "Limit as x->a" in task:
            fields = [("Function f(x)", "(x^2 - 4)/(x - 2)"), ("Point a", "2")]
        elif "Limit at Infinity" in task:
            fields = [("Function f(x)", "(2*x^2 + 1)/(x^2 - 3)")]
        elif "Left/Right" in task:
            fields = [("Function f(x)", "1/x"), ("Point a", "0"), ("Direction (+ or -)", "+")]

        # --- DIFFERENTIATION ---
        elif "Find Derivative" in task:
            fields = [("Function f(x)", "x^3 + 2*x^2 - 5")]
        elif "Implicit" in task:
            fields = [("Equation F(x,y)=0", "x^2 + y^2 - 25")]
        elif "Tangent Line" in task:
            fields = [("Function f(x)", "x^2"), ("Point x=a", "1")]
        elif "Higher Order" in task:
            fields = [("Function f(x)", "sin(x)"), ("Order n", "2")]

        # --- INTEGRALS ---
        elif "Indefinite" in task:
            fields = [("Function f(x)", "x^2 + 1/x")]
        elif "Definite" in task:
            fields = [("Function f(x)", "x^2"), ("Lower Limit a", "0"), ("Upper Limit b", "3")]
        elif "Area Under Curve" in task:
             fields = [("Function f(x)", "x^2"), ("Lower Limit a", "0"), ("Upper Limit b", "3")]

        # --- DIFFERENTIAL EQUATIONS ---
        elif "Separable" in task:
            fields = [("Equation (use y')", "y' = x*y")]
        elif "Growth/Decay" in task:
            fields = [("Initial Amount y0", "100"), ("Rate k", "0.05"), ("Time t", "10")]

        # --- PARTIAL DERIVATIVES ---
        elif "Partial" in task:
            fields = [("Function f(x,y)", "x^2*y + sin(y)")]

        # Create Entry Boxes
        for text, default in fields:
            row = tk.Frame(self.inputFrame, bg=backgroundColour)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=text, width=20, anchor="w", bg=backgroundColour, fg=accentColour, font=("Arial", 9, "bold")).pack(side="left")
            ent = tk.Entry(row, bg=buttonBg, fg="white", insertbackground=accentColour, relief="flat", font=("Arial", 10))
            ent.insert(0, default)
            ent.pack(side="right", fill="x", expand=True)
            self.entries[text] = ent

    def solve_step_by_step(self):
        task = self.taskVar.get()
        steps = ""
        
        try:
            # Collect inputs
            inputs = {k: v.get() for k, v in self.entries.items()}
            x, y, z = symbols('x y z')
        except ValueError:
            messagebox.showerror("Input Error", "Please check your inputs.")
            return

        try:
            # ================= LIMITS =================
            if "Limit as x->a" in task:
                expr_str = inputs["Function f(x)"]
                a = float(inputs["Point a"])
                f = sympy.sympify(expr_str)
                res = limit(f, x, a)
                
                steps += f"TOPIC: LIMIT OF A FUNCTION\n--------------------------\n"
                steps += f"Calculate limit of f(x) = {expr_str} as x -> {a}\n\n"
                steps += "1. Direct Substitution Check:\n"
                try:
                    val = f.subs(x, a)
                    steps += f"   f({a}) = {val}\n"
                except:
                    steps += f"   f({a}) is undefined or indeterminate.\n"
                
                steps += f"\n2. Calculated Limit:\n   lim(x->{a}) = {res}\n"

            elif "Limit at Infinity" in task:
                expr_str = inputs["Function f(x)"]
                f = sympy.sympify(expr_str)
                res = limit(f, x, sympy.oo)
                
                steps += "TOPIC: LIMIT AT INFINITY\n------------------------\n"
                steps += f"Calculate limit of f(x) = {expr_str} as x -> oo\n\n"
                steps += f"Result: {res}\n"

            # ================= DIFFERENTIATION =================
            elif "Find Derivative" in task:
                expr_str = inputs["Function f(x)"]
                f = sympy.sympify(expr_str)
                res = diff(f, x)
                
                steps += "TOPIC: DIFFERENTIATION\n----------------------\n"
                steps += f"Function: f(x) = {expr_str}\n\n"
                steps += "1. Apply Differentiation Rules:\n"
                steps += f"   f'(x) = d/dx [{expr_str}]\n\n"
                steps += f"Result:\n   f'(x) = {res}\n"

            elif "Tangent Line" in task:
                expr_str = inputs["Function f(x)"]
                a = float(inputs["Point x=a"])
                f = sympy.sympify(expr_str)
                
                # 1. Find f(a)
                fa = f.subs(x, a)
                # 2. Find f'(x)
                f_prime = diff(f, x)
                # 3. Find slope m = f'(a)
                m = f_prime.subs(x, a)
                
                steps += "TOPIC: TANGENT LINE\n-------------------\n"
                steps += f"Find tangent to f(x) = {expr_str} at x = {a}\n\n"
                steps += f"1. Find point coordinates:\n   f({a}) = {fa}\n   Point: ({a}, {fa})\n\n"
                steps += f"2. Find Derivative (Slope function):\n   f'(x) = {f_prime}\n\n"
                steps += f"3. Calculate Slope at x={a}:\n   m = f'({a}) = {m}\n\n"
                steps += f"4. Equation of Line (y - y1 = m(x - x1)):\n"
                steps += f"   y - {fa} = {m}(x - {a})\n"
                steps += f"   y = {m}*x + ({fa - m*a})\n"

            # ================= INTEGRALS =================
            elif "Indefinite Integral" in task:
                expr_str = inputs["Function f(x)"]
                f = sympy.sympify(expr_str)
                res = integrate(f, x)
                
                steps += "TOPIC: INDEFINITE INTEGRAL\n--------------------------\n"
                steps += f"Integral of: {expr_str} dx\n\n"
                steps += "1. Find Antiderivative:\n"
                steps += f"   F(x) = {res} + C\n"

            elif "Definite Integral" in task:
                expr_str = inputs["Function f(x)"]
                a = float(inputs["Lower Limit a"])
                b = float(inputs["Upper Limit b"])
                f = sympy.sympify(expr_str)
                
                F = integrate(f, x)
                val_b = F.subs(x, b)
                val_a = F.subs(x, a)
                res = val_b - val_a
                
                steps += "TOPIC: DEFINITE INTEGRAL\n------------------------\n"
                steps += f"Calculate Integral from {a} to {b} of {expr_str} dx\n\n"
                steps += f"1. Find Antiderivative F(x):\n   F(x) = {F}\n\n"
                steps += f"2. Apply Fundamental Theorem (F(b) - F(a)):\n"
                steps += f"   F({b}) = {val_b}\n"
                steps += f"   F({a}) = {val_a}\n\n"
                steps += f"3. Result:\n   {val_b} - ({val_a}) = {res}\n"

            # ================= PARTIAL DERIVATIVES =================
            elif "Partial Derivative" in task:
                expr_str = inputs["Function f(x,y)"]
                f = sympy.sympify(expr_str)
                
                if "fx" in task:
                    res = diff(f, x)
                    var = "x"
                else:
                    res = diff(f, y)
                    var = "y"
                
                steps += f"TOPIC: PARTIAL DERIVATIVE ({var})\n-----------------------------\n"
                steps += f"Function f(x,y) = {expr_str}\n\n"
                steps += f"Differentiate with respect to {var} (treating other variables as constants):\n\n"
                steps += f"Result:\n   df/d{var} = {res}\n"

            else:
                steps += "Solver logic for this specific task is coming soon."

        except Exception as e:
            steps += f"Error in calculation: {str(e)}\nCheck your syntax (e.g., use * for multiply, ** for power)."

        self.solutionText.delete("1.0", "end")
        self.solutionText.insert("1.0", steps)

    def clearInputs(self):
        self.updateInputFields()
        self.solutionText.delete("1.0", "end")

    def on_close(self, parent):
        parent.attributes('-disabled', False)
        self.destroy()