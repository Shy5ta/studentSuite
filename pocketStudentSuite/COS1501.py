import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import itertools

#+++++++++++++++ Color Scheme +++++++++++++++++++
backgroundColour = '#282c34'
foregroundColour = '#c6c6c6'
accentColour = '#61afef'
buttonBg = '#3c424a'
buttonHover = '#4a5260'

#+++++++++++++++ COS1501 Solver Window +++++++++++++++++++
class COS1501Window(tk.Toplevel):
    def __init__(self, parent, topicName):
        super().__init__(parent)
        
        self.title(f"COS1501 - {topicName}")
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
            text=f"💻 {self.topicName}",
            font=("Arial", 18, "bold"),
            bg=backgroundColour,
            fg=accentColour
        ).pack()
        
        tk.Label(
            headerFrame,
            text="Discrete Mathematics & Logic Tools",
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
            text="Result / Truth Table:", 
            bg=backgroundColour, 
            fg=foregroundColour,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.solutionText = scrolledtext.ScrolledText(
            rightPanel,
            font=("Courier", 10), # Monospace for tables
            bg='#1e1e1e',
            fg=foregroundColour,
            wrap="none", # Important for truth tables
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
        if "Logic" in self.topicName:
            return ["Generate Truth Table", "Check Tautology/Contradiction"]
        elif "Sets" in self.topicName:
            return ["Set Operations (Union, Intersect)", "Power Set Generator", "Check Subset"]
        elif "Relations" in self.topicName:
            return ["Check Properties (Reflexive, etc.)", "Find Inverse Relation", "Composition of Relations"]
        elif "Functions" in self.topicName:
            return ["Check Function Properties"]
        else:
            return ["Standard Tool"]

    def updateInputFields(self, event=None):
        for widget in self.inputFrame.winfo_children():
            widget.destroy()
        self.entries = {}
        
        task = self.taskVar.get()
        fields = []
        
        # --- LOGIC ---
        if "Truth Table" in task or "Tautology" in task:
            tk.Label(self.inputFrame, text="Use: p, q, r, &, |, ~, ->, <->", bg=backgroundColour, fg=foregroundColour).pack()
            fields = [("Expression", "(p -> q) & (q -> r)")]

        # --- SETS ---
        elif "Set Operations" in task:
            tk.Label(self.inputFrame, text="Elements: 1,2,3 or a,b,c", bg=backgroundColour, fg=foregroundColour).pack()
            fields = [("Set A", "1, 2, 3"), ("Set B", "3, 4, 5")]
        elif "Power Set" in task:
            fields = [("Set A", "a, b, c")]
        elif "Check Subset" in task:
            fields = [("Set A", "1, 2"), ("Set B", "1, 2, 3, 4")]

        # --- RELATIONS ---
        elif "Check Properties" in task:
            tk.Label(self.inputFrame, text="Set A: 1,2,3\nRelation R: (1,1), (1,2)...", bg=backgroundColour, fg=foregroundColour).pack()
            fields = [("Set A", "1, 2, 3"), ("Relation R", "(1,1), (2,2), (3,3), (1,2)")]
        elif "Inverse Relation" in task:
             fields = [("Relation R", "(1,a), (2,b), (3,c)")]
        elif "Composition" in task:
             fields = [("Relation R", "(1,a), (2,b)"), ("Relation S", "(a,x), (b,y)")]

        # --- FUNCTIONS ---
        elif "Check Function" in task:
            fields = [("Domain A", "1, 2, 3"), ("Codomain B", "a, b, c, d"), ("Function f (pairs)", "(1,a), (2,b), (3,c)")]

        # Create Entry Boxes
        for text, default in fields:
            row = tk.Frame(self.inputFrame, bg=backgroundColour)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=text, width=15, anchor="w", bg=backgroundColour, fg=accentColour, font=("Arial", 9, "bold")).pack(side="left")
            ent = tk.Entry(row, bg=buttonBg, fg="white", insertbackground=accentColour, relief="flat", font=("Arial", 10))
            ent.insert(0, default)
            ent.pack(side="right", fill="x", expand=True)
            self.entries[text] = ent

    def solve_step_by_step(self):
        task = self.taskVar.get()
        output = ""
        
        try:
            inputs = {k: v.get() for k, v in self.entries.items()}
        except:
            return

        try:
            # ================= LOGIC =================
            if "Truth Table" in task or "Tautology" in task:
                expr_str = inputs["Expression"]
                
                # Parse variables
                vars = sorted(list(set([c for c in expr_str if c.isalpha()])))
                n = len(vars)
                
                # Logic Evaluator
                def evaluate_logic(expression, values):
                    # Convert custom symbols to Python logic
                    e = expression.replace("&", " and ").replace("|", " or ").replace("~", " not ")
                    # Implication A -> B is equivalent to (not A) or B. 
                    # For Truth tables, we can use <= for Implication (True <= False is False)
                    e = e.replace("->", "<=").replace("<->", "==")
                    
                    env = {k: v for k, v in zip(vars, values)}
                    return eval(e, {}, env)

                # Header
                header = " | ".join(vars) + " || Result\n"
                output += header + "-" * len(header) + "\n"
                
                results = []
                combinations = list(itertools.product([True, False], repeat=n))
                
                for combo in combinations:
                    res = evaluate_logic(expr_str, combo)
                    results.append(res)
                    
                    row_str = " | ".join(["T" if v else "F" for v in combo])
                    res_str = "T" if res else "F"
                    output += f"{row_str} || {res_str}\n"

                if "Tautology" in task:
                    if all(results): output += "\nConclusion: TAUTOLOGY (Always True)"
                    elif not any(results): output += "\nConclusion: CONTRADICTION (Always False)"
                    else: output += "\nConclusion: CONTINGENCY (Sometimes True/False)"

            # ================= SETS =================
            elif "Set Operations" in task:
                A = set(x.strip() for x in inputs["Set A"].split(","))
                B = set(x.strip() for x in inputs["Set B"].split(","))
                
                output += f"Set A: {A}\nSet B: {B}\n\n"
                output += f"Union (A u B): {A.union(B)}\n"
                output += f"Intersection (A n B): {A.intersection(B)}\n"
                output += f"Difference (A - B): {A.difference(B)}\n"
                output += f"Difference (B - A): {B.difference(A)}\n"
                output += f"Symmetric Diff (A + B): {A.symmetric_difference(B)}\n"

            elif "Power Set" in task:
                A = [x.strip() for x in inputs["Set A"].split(",")]
                n = len(A)
                powerset = []
                for i in range(1 << n):
                    subset = [A[j] for j in range(n) if (i & (1 << j))]
                    powerset.append(set(subset))
                
                output += f"Power Set P(A) (Size 2^{n} = {len(powerset)}):\n\n"
                for s in powerset:
                    output += f"{s}\n"

            # ================= RELATIONS =================
            elif "Check Properties" in task:
                A = set(x.strip() for x in inputs["Set A"].split(","))
                # Parse Relation: (1,1), (1,2) -> list of tuples
                raw_R = inputs["Relation R"].replace("(", "").replace(")", "")
                pairs = [tuple(p.split(",")) for p in raw_R.split(" ") if "," in p]
                # Clean pairs
                R = set()
                for a, b in pairs:
                    R.add((a.strip(), b.strip()))
                
                output += f"Relation R: {R}\n\n"
                
                # Reflexive
                is_refl = all((a, a) in R for a in A)
                output += f"Reflexive: {'YES' if is_refl else 'NO'}\n"

                # Symmetric
                is_sym = all((b, a) in R for (a, b) in R)
                output += f"Symmetric: {'YES' if is_sym else 'NO'}\n"

                # Transitive
                is_trans = True
                missing_trans = []
                for (a, b) in R:
                    for (c, d) in R:
                        if b == c: # (a,b) and (b,d) exist
                            if (a, d) not in R:
                                is_trans = False
                                missing_trans.append(((a,b), (b,d)))
                
                output += f"Transitive: {'YES' if is_trans else 'NO'}\n"
                if not is_trans:
                    output += f"  Counterexample: {missing_trans[0]} exists, but transitive pair missing.\n"

            # ================= FUNCTIONS =================
            elif "Check Function" in task:
                A = set(x.strip() for x in inputs["Domain A"].split(","))
                B = set(x.strip() for x in inputs["Codomain B"].split(","))
                
                raw_f = inputs["Function f (pairs)"].replace("(", "").replace(")", "")
                pairs = [tuple(p.split(",")) for p in raw_f.split(" ") if "," in p]
                
                f = {}
                valid_func = True
                for a, b in pairs:
                    a, b = a.strip(), b.strip()
                    if a in f: valid_func = False # One-to-many check
                    f[a] = b
                
                # Domain Check
                if set(f.keys()) != A: 
                    output += "NOT a Function (Domain mismatch)\n"
                elif not valid_func:
                    output += "NOT a Function (One element maps to multiple)\n"
                else:
                    output += "Valid Function: YES\n"
                    
                    # Injective (One-to-One)
                    values = list(f.values())
                    is_inj = len(values) == len(set(values))
                    output += f"Injective: {'YES' if is_inj else 'NO'}\n"
                    
                    # Surjective (Onto)
                    is_sur = set(values) == B
                    output += f"Surjective: {'YES' if is_sur else 'NO'}\n"
                    
                    # Bijective
                    output += f"Bijective: {'YES' if (is_inj and is_sur) else 'NO'}\n"

            else:
                output += "Logic coming soon."

        except Exception as e:
            output += f"Error: {str(e)}\nCheck input format."

        self.solutionText.delete("1.0", "end")
        self.solutionText.insert("1.0", output)

    def clearInputs(self):
        self.updateInputFields()
        self.solutionText.delete("1.0", "end")

    def on_close(self, parent):
        parent.attributes('-disabled', False)
        self.destroy()