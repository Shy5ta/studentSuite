import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sympy
from sympy import symbols, limit, diff, integrate, series, sin, cos, tan, exp, log, oo, pi, asin, acos, atan, sinh, cosh, tanh

#+++++++++++++++ Color Scheme +++++++++++++++++++
backgroundColour = '#282c34'
foregroundColour = '#c6c6c6'
accentColour = '#61afef'
buttonBg = '#3c424a'
buttonHover = '#4a5260'

#+++++++++++++++ MAT1613 Solver Window +++++++++++++++++++
class MAT1613Window(tk.Toplevel):
    def __init__(self, parent, topicName):
        super().__init__(parent)
        
        self.title(f"MAT1613 - {topicName}")
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
            text="Calculus B: Advanced Integration & Applications",
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
        # Return tasks based on the Topic Name
        if "Derivative" in self.topicName: # Applications of Derivatives
            return ["L'Hopital's Rule (Limits)", "Mean Value Theorem Check", "Find Critical Points"]
        elif "Transcendental" in self.topicName:
            return ["Derive Inverse Trig", "Derive Hyperbolic Func", "Integrate Hyperbolic"]
        elif "Integration" in self.topicName: # Techniques
            return ["Integration by Parts", "Partial Fractions", "Trig Substitution (Placeholder)", "Improper Integral Check"]
        elif "Applications" in self.topicName: # Area/Volume
            return ["Area Between Curves", "Volume of Revolution (Disk)"]
        elif "Series" in self.topicName:
            return ["Taylor Series Expansion", "Limit of Sequence"]
        else:
            return ["Standard Calculation"]

    def updateInputFields(self, event=None):
        for widget in self.inputFrame.winfo_children():
            widget.destroy()
        self.entries = {}
        
        task = self.taskVar.get()
        fields = []
        
        # --- DERIVATIVES & LIMITS ---
        if "L'Hopital" in task:
            fields = [("Function f(x)", "(sin(x) - x)/x**3"), ("Limit Point a", "0")]
        elif "Mean Value" in task:
            fields = [("Function f(x)", "x**3 - x"), ("Interval [a, b]", "-1, 2")]
        elif "Critical Points" in task:
            fields = [("Function f(x)", "x**3 - 3*x**2 + 1")]

        # --- TRANSCENDENTAL ---
        elif "Derive Inverse" in task:
            fields = [("Function y", "asin(x**2)")]
        elif "Derive Hyperbolic" in task:
            fields = [("Function y", "sinh(3*x)")]

        # --- INTEGRATION TECHNIQUES ---
        elif "Integration by Parts" in task:
            fields = [("Integrand f(x)", "x * exp(x)"), ("Parts u", "x"), ("Parts dv", "exp(x)")]
        elif "Partial Fractions" in task:
            fields = [("Rational Function", "1 / (x**2 - 1)")]
        elif "Improper" in task:
            fields = [("Integrand", "1/x**2"), ("Lower Limit", "1"), ("Upper Limit", "oo")]

        # --- AREA & VOLUME ---
        elif "Area Between" in task:
            fields = [("Upper Function f(x)", "x"), ("Lower Function g(x)", "x**2"), ("Interval a, b", "0, 1")]
        elif "Volume" in task:
            fields = [("Radius Function R(x)", "sqrt(x)"), ("Interval a, b", "0, 1")]

        # --- SERIES ---
        elif "Taylor Series" in task:
            fields = [("Function f(x)", "sin(x)"), ("Point a", "0"), ("Order n", "5")]
        elif "Sequence" in task:
            fields = [("General Term a_n", "(n + 1)/n")]

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
        x, n = symbols('x n')
        
        try:
            inputs = {k: v.get() for k, v in self.entries.items()}
        except:
            return

        try:
            # ================= DERIVATIVES & LIMITS =================
            if "L'Hopital" in task:
                func_str = inputs["Function f(x)"]
                pt = float(inputs["Limit Point a"])
                f = sympy.sympify(func_str)
                
                # Check direct sub
                try:
                    val = f.subs(x, pt)
                except:
                    val = "undefined"
                
                # Calculate Limit
                lim_val = limit(f, x, pt)
                
                steps += "TOPIC: L'HOPITAL'S RULE\n-----------------------\n"
                steps += f"Limit of {func_str} as x -> {pt}\n\n"
                steps += f"1. Direct Substitution: {val}\n"
                steps += "   (Likely 0/0 or inf/inf)\n\n"
                steps += f"2. Applying L'Hopital (differentiating num and denom)...\n"
                steps += f"   Limit Value = {lim_val}\n"

            # ================= INTEGRATION TECHNIQUES =================
            elif "Integration by Parts" in task:
                func_str = inputs["Integrand f(x)"]
                u_str = inputs["Parts u"]
                dv_str = inputs["Parts dv"]
                
                f = sympy.sympify(func_str)
                u = sympy.sympify(u_str)
                dv = sympy.sympify(dv_str)
                
                du = diff(u, x)
                v = integrate(dv, x)
                
                result = u*v - integrate(v*du, x)
                
                steps += "TOPIC: INTEGRATION BY PARTS\n---------------------------\n"
                steps += f"Integral: {func_str} dx\n"
                steps += "Formula: integral(u dv) = uv - integral(v du)\n\n"
                steps += f"1. Choose u = {u}  =>  du = {du} dx\n"
                steps += f"2. Choose dv = {dv} dx =>  v = {v}\n\n"
                steps += f"3. Apply Formula:\n"
                steps += f"   = ({u})*({v}) - integral({v} * {du})\n"
                steps += f"   = {u*v} - {integrate(v*du, x)}\n\n"
                steps += f"Final Result: {result} + C\n"

            elif "Partial Fractions" in task:
                func_str = inputs["Rational Function"]
                f = sympy.sympify(func_str)
                part_frac = sympy.apart(f)
                integral = integrate(part_frac, x)
                
                steps += "TOPIC: PARTIAL FRACTIONS\n------------------------\n"
                steps += f"Integrate: {func_str}\n\n"
                steps += f"1. Decompose into Partial Fractions:\n"
                steps += f"   {part_frac}\n\n"
                steps += f"2. Integrate each term:\n"
                steps += f"   {integral} + C\n"

            elif "Improper" in task:
                func_str = inputs["Integrand"]
                a_str = inputs["Lower Limit"]
                b_str = inputs["Upper Limit"]
                
                f = sympy.sympify(func_str)
                # Handle infinity input
                if "oo" in b_str: b = oo
                else: b = float(b_str)
                a = float(a_str)
                
                res = integrate(f, (x, a, b))
                
                steps += "TOPIC: IMPROPER INTEGRAL\n------------------------\n"
                steps += f"Integral from {a} to {b} of {func_str}\n\n"
                steps += "1. Set up Limit:\n"
                steps += f"   lim(t->{b}) integral({a} to t)\n\n"
                steps += f"2. Evaluate:\n"
                if res == oo:
                    steps += "   Result is Infinity (DIVERGES)\n"
                else:
                    steps += f"   Result = {res} (CONVERGES)\n"

            # ================= APPLICATIONS =================
            elif "Volume" in task:
                r_str = inputs["Radius Function R(x)"]
                a_str, b_str = inputs["Interval a, b"].split(",")
                
                R = sympy.sympify(r_str)
                a, b = float(a_str), float(b_str)
                
                vol = sympy.pi * integrate(R**2, (x, a, b))
                
                steps += "TOPIC: VOLUME OF REVOLUTION (DISK)\n----------------------------------\n"
                steps += f"Rotate region under {r_str} about x-axis.\n"
                steps += "Formula: V = pi * integral(R(x)^2 dx)\n\n"
                steps += f"1. R(x)^2 = ({R})**2 = {R**2}\n"
                steps += f"2. Integrate from {a} to {b}:\n"
                steps += f"   V = {vol} cubic units\n"
                steps += f"   V approx {vol.evalf():.4f}\n"

            # ================= SERIES =================
            elif "Taylor Series" in task:
                func_str = inputs["Function f(x)"]
                a = float(inputs["Point a"])
                order = int(inputs["Order n"])
                f = sympy.sympify(func_str)
                
                ser = f.series(x, a, order).removeO()
                
                steps += "TOPIC: TAYLOR SERIES\n--------------------\n"
                steps += f"Expand {func_str} at x={a} to order {order}\n\n"
                steps += f"Resulting Polynomial:\n"
                steps += f"{ser}\n"

            else:
                steps += "Solution logic coming soon."

        except Exception as e:
            steps += f"Calculation Error: {str(e)}\nCheck syntax (e.g. use ** for power)"

        self.solutionText.delete("1.0", "end")
        self.solutionText.insert("1.0", steps)

    def clearInputs(self):
        self.updateInputFields()
        self.solutionText.delete("1.0", "end")

    def on_close(self, parent):
        parent.attributes('-disabled', False)
        self.destroy()