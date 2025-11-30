import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import sympy
from sympy import symbols, Function, Eq, classify_ode, dsolve, separatevars, solve

#+++++++++++++++ Color Scheme +++++++++++++++++++
backgroundColour = '#282c34'
foregroundColour = '#c6c6c6'
accentColour = '#61afef'
buttonBg = '#3c424a'
buttonHover = '#4a5260'

#+++++++++++++++ APM1514 Solver Window +++++++++++++++++++
class APM1514Window(tk.Toplevel):
    def __init__(self, parent, topicName):
        super().__init__(parent)
        
        self.title(f"APM1514 - {topicName}")
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
            text="Select a model or check equation separability",
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

        # Model Selector
        tk.Label(
            leftPanel, 
            text="Select Task:", 
            bg=backgroundColour, 
            fg=foregroundColour,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 5))
        
        self.modelVar = tk.StringVar()
        models = self.getModels()
        self.modelVar.set(models[0])
        
        dropdown = ttk.Combobox(leftPanel, textvariable=self.modelVar, values=models, state="readonly", width=35)
        dropdown.pack(fill="x", pady=(0, 15))
        dropdown.bind("<<ComboboxSelected>>", self.updateInputFields)

        # Input Fields Container
        self.inputFrame = tk.LabelFrame(
            leftPanel, 
            text="Input", 
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
            text="📝 Solve / Analyze",
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

    def getModels(self):
        # Specific models + General Tools based on Syllabus
        base_models = []
        if "Population" in self.topicName:
            base_models = ["Malthusian Growth (Find P)", "Malthusian Growth (Find time t)", "Logistic Growth", "Harvesting Model"]
        elif "Cooling" in self.topicName:
            base_models = ["Newton's Law (Find Temp)", "Newton's Law (Find time t)"]
        elif "Discrete" in self.topicName:
            base_models = ["Linear Difference Eq", "Savings Account", "Loan Repayment"]
        elif "Predator" in self.topicName:
            base_models = ["Predator-Prey"]
        else:
            base_models = ["Malthusian Growth"]
            
        # Add the Separability Checker to all Differential Equation topics
        return ["🔍 Check Separability"] + base_models

    def updateInputFields(self, event=None):
        # Dynamic inputs based on model
        for widget in self.inputFrame.winfo_children():
            widget.destroy()
        self.entries = {}
        
        model = self.modelVar.get()
        fields = []
        
        if "Check Separability" in model:
            # Special case for equation input
            tk.Label(
                self.inputFrame, 
                text="Enter Differential Equation:\n(Use formats like: dy/dx = x*y  or  y' = x + y)", 
                anchor="w", bg=backgroundColour, fg=accentColour, font=("Arial", 9, "bold")
            ).pack(fill="x")
            
            ent = tk.Entry(
                self.inputFrame, bg=buttonBg, fg="white", 
                insertbackground=accentColour, relief="flat", font=("Arial", 11)
            )
            ent.insert(0, "dy/dx = y * (1 - y)")
            ent.pack(fill="x", ipady=5, pady=5)
            self.entries["Equation"] = ent
            return

        # --- Standard Model Fields ---
        if "Malthusian Growth (Find P)" == model:
            fields = [("Initial Pop (P0)", "100"), ("Growth Rate k", "0.02"), ("Time t", "10")]
        elif "Malthusian Growth (Find time t)" == model:
            fields = [("Initial Pop (P0)", "100"), ("Target Pop P(t)", "200"), ("Growth Rate k", "0.02")]
        elif "Logistic Growth" == model:
            fields = [("Initial Pop (P0)", "100"), ("Growth Rate a", "0.2"), ("Interaction b", "0.0001"), ("Time t", "5")]
        elif "Harvesting Model" == model:
            fields = [("Initial Pop (P0)", "100"), ("Growth Rate k", "0.1"), ("Harvest Rate h", "5")]
        elif "Newton's Law (Find Temp)" == model:
            fields = [("Initial Temp (T0)", "100"), ("Ambient Temp (Tm)", "20"), ("Constant k", "0.1"), ("Time t", "10")]
        elif "Newton's Law (Find time t)" == model:
            fields = [("Initial Temp (T0)", "100"), ("Ambient Temp (Tm)", "20"), ("Constant k", "0.1"), ("Target Temp", "50")]
        elif "Linear Difference" in model:
            fields = [("Initial Value (a0)", "5"), ("Multiplier r", "2"), ("Steps n", "4")]
        elif "Savings Account" in model:
            fields = [("Initial Deposit (A0)", "1000"), ("Interest Rate % (q)", "5"), ("Monthly Deposit (D)", "100"), ("Months n", "12")]
        elif "Loan Repayment" in model:
            fields = [("Loan Amount (L)", "10000"), ("Interest Rate % (q)", "1.5"), ("Monthly Payment (P)", "200"), ("Months n", "12")]
        elif "Predator-Prey" in model:
            fields = [("Prey (x)", "40"), ("Predator (y)", "9"), ("Alpha", "0.1"), ("Beta", "0.02"), ("Gamma", "0.1"), ("Delta", "0.01")]

        for text, default in fields:
            row = tk.Frame(self.inputFrame, bg=backgroundColour)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=text, anchor="w", bg=backgroundColour, fg=accentColour, font=("Arial", 9, "bold")).pack(fill="x")
            ent = tk.Entry(row, bg=buttonBg, fg="white", insertbackground=accentColour, relief="flat", font=("Arial", 10))
            ent.insert(0, default)
            ent.pack(fill="x", ipady=4)
            self.entries[text] = ent

    def solve_step_by_step(self):
        model = self.modelVar.get()
        steps = ""

        # ================= SEPARABILITY CHECKER =================
        if "Check Separability" in model:
            eq_str = self.entries["Equation"].get()
            steps = self.check_separability(eq_str)
            self.solutionText.delete("1.0", "end")
            self.solutionText.insert("1.0", steps)
            return

        # ================= STANDARD SOLVERS =================
        try:
            data = {}
            for label, entry in self.entries.items():
                data[label] = float(entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure all fields contain valid numbers.")
            return

        if "Malthusian Growth" in model:
            P0 = data["Initial Pop (P0)"]
            k = data["Growth Rate k"]
            steps += "TOPIC: MALTHUSIAN POPULATION MODEL\n----------------------------------\n"
            steps += "1. Differential Equation: dP/dt = kP\n"
            steps += "2. General Solution: P(t) = P0 * e^(kt)\n"
            
            if "Find P" in model:
                t = data["Time t"]
                result = P0 * math.exp(k * t)
                steps += f"3. Solve for t={t}:\n   P({t}) = {P0} * e^({k}*{t})\n   Result = {result:.2f}"
            else:
                Pt = data["Target Pop P(t)"]
                ratio = Pt/P0
                t_calc = math.log(ratio) / k
                steps += f"3. Solve for t given P={Pt}:\n   {Pt} = {P0}e^({k}t)\n   ln({ratio:.2f}) = {k}t\n   t = {t_calc:.2f}"

        elif "Logistic" in model:
            P0 = data["Initial Pop (P0)"]
            a = data["Growth Rate a"]
            b = data["Interaction b"]
            t = data["Time t"]
            K = a/b
            A = (K - P0)/P0
            result = K / (1 + A * math.exp(-a * t))
            
            steps += "TOPIC: LOGISTIC POPULATION MODEL\n--------------------------------\n"
            steps += "1. Differential Equation: dP/dt = aP - bP^2\n"
            steps += f"2. Carrying Capacity K = a/b = {K:.2f}\n"
            steps += f"3. Constant A = (K-P0)/P0 = {A:.4f}\n"
            steps += f"4. Solution P(t) = K / (1 + A*e^(-at))\n"
            steps += f"   P({t}) = {K:.2f} / (1 + {A:.4f}*e^(-{a}*{t}))\n"
            steps += f"   Result = {result:.2f}"

        elif "Newton" in model:
            T0 = data["Initial Temp (T0)"]
            Tm = data["Ambient Temp (Tm)"]
            k = data["Constant k"]
            steps += "TOPIC: NEWTON'S LAW OF COOLING\n------------------------------\n"
            steps += "1. Equation: dT/dt = -k(T - Tm)\n"
            steps += "2. Solution: T(t) = Tm + (T0 - Tm)e^(-kt)\n"
            
            if "Find Temp" in model:
                t = data["Time t"]
                res = Tm + (T0-Tm)*math.exp(-k*t)
                steps += f"3. T({t}) = {Tm} + ({T0}-{Tm})e^(-{k}*{t})\n   Result = {res:.2f}"
            else:
                Target = data["Target Temp"]
                ratio = (Target - Tm)/(T0 - Tm)
                t_calc = math.log(ratio) / -k
                steps += f"3. Solve for t:\n   {Target} = {Tm} + {T0-Tm}e^(-{k}t)\n   t = {t_calc:.2f}"

        elif "Linear Difference" in model:
            a0, r, n = data["Initial Value (a0)"], data["Multiplier r"], int(data["Steps n"])
            steps += "TOPIC: LINEAR DIFFERENCE EQUATION\n---------------------------------\n"
            steps += f"1. Equation: a(n+1) = {r} * a(n)\n"
            steps += f"2. Solution: a(n) = {a0} * ({r})^n\n"
            steps += f"3. Result a({n}) = {a0 * (r**n)}"

        elif "Savings" in model:
            A0, q, D, n = data["Initial Deposit (A0)"], data["Interest Rate % (q)"], data["Monthly Deposit (D)"], int(data["Months n"])
            r = 1 + q/100
            steps += "TOPIC: SAVINGS ACCOUNT\n----------------------\n"
            steps += f"1. Recurrence: A(n+1) = {r}*A(n) + {D}\n"
            curr = A0
            for i in range(1, n+1):
                curr = curr*r + D
                if i <= 3 or i==n: steps += f"   Month {i}: {curr:.2f}\n"

        elif "Loan" in model:
            L, q, P, n = data["Loan Amount (L)"], data["Interest Rate % (q)"], data["Monthly Payment (P)"], int(data["Months n"])
            r = 1 + q/100
            steps += "TOPIC: LOAN REPAYMENT\n---------------------\n"
            steps += f"1. Recurrence: A(n+1) = {r}*A(n) - {P}\n"
            curr = L
            for i in range(1, n+1):
                curr = curr*r - P
                if i <= 3 or i==n: steps += f"   Month {i}: {curr:.2f}\n"

        else:
            steps = "Solution logic for this model coming soon."

        self.solutionText.delete("1.0", "end")
        self.solutionText.insert("1.0", steps)

    def check_separability(self, eq_str):
        # Uses SymPy to analyze the equation string
        steps = f"ANALYZING: {eq_str}\n"
        steps += "--------------------------------------\n"
        
        try:
            x = symbols('x')
            y = Function('y')(x)
            
            # Pre-process string to make it SymPy friendly
            eq_str = eq_str.replace("dy/dx", "y'").replace("^", "**")
            
            # Extract RHS (assuming y' = ...)
            if "=" in eq_str:
                rhs_str = eq_str.split("=")[1].strip()
            else:
                rhs_str = eq_str
                
            # Parse
            rhs = sympy.sympify(rhs_str, locals={'y': y, 'x': x})
            ode = Eq(y.diff(x), rhs)
            
            steps += "1. Standard Form:\n"
            steps += f"   dy/dx = {rhs}\n\n"
            
            # Check Classification
            hints = classify_ode(ode)
            
            if "separable" in hints:
                steps += "✅ RESULT: SEPARABLE\n\n"
                
                # Attempt to separate
                # Sympy's separatevars takes an expression, returns g(x)*h(y) if separable
                separated = separatevars(rhs)
                
                if separated:
                    steps += "2. Separation Logic:\n"
                    steps += f"   The expression factors into: {separated}\n"
                    steps += "   We can write this as: 1/h(y) dy = g(x) dx\n\n"
                    
                    # Solve
                    sol = dsolve(ode, hint='separable')
                    steps += "3. General Solution:\n"
                    steps += f"   {sol}"
                else:
                    steps += "   (Could not automatically display separated terms, but it is valid.)"
            else:
                steps += "❌ RESULT: NOT SEPARABLE\n"
                steps += f"   Reason: Cannot factor f(x,y) into g(x)*h(y).\n"
                steps += f"   Other classifications found: {hints}"
                
        except Exception as e:
            steps += f"\nError parsing equation: {str(e)}\n"
            steps += "Tip: Use python syntax (e.g., x*y instead of xy, x**2 for x^2)"
            
        return steps

    def clearInputs(self):
        self.updateInputFields()
        self.solutionText.delete("1.0", "end")

    def on_close(self, parent):
        parent.attributes('-disabled', False)
        self.destroy()