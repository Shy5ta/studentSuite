import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

#+++++++++++++++ Color Scheme +++++++++++++++++++
backgroundColour = '#282c34'
foregroundColour = '#c6c6c6'
accentColour = '#61afef'
buttonBg = '#3c424a'
buttonHover = '#4a5260'

# Configure ttk styles for better appearance
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook', background=backgroundColour, borderwidth=0)
style.configure('TNotebook.Tab', background=buttonBg, foreground=foregroundColour, 
                padding=[10, 5], font=('Arial', 10))
style.map('TNotebook.Tab', background=[('selected', accentColour)], 
          foreground=[('selected', 'white')])

#+++++++++++++++ APM1513 Problem Solver Window +++++++++++++++++++
class APM1513Window(tk.Toplevel):
    def __init__(self, parent, topicName):
        # This initializes the problem solver window
        super().__init__(parent)
        
        self.title(f"APM1513 - {topicName}")
        self.geometry("800x650")
        self.configure(bg=backgroundColour)
        
        # Disable the module window while this is open
        parent.attributes('-disabled', True)
        
        # Protocol to run when the user closes the window
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close(parent))
        
        # Store the topic name for reference
        self.topicName = topicName
        
        # Create the appropriate interface based on topic
        self.createInterface()
    
    def createInterface(self):
        # Header section with topic name
        headerFrame = tk.Frame(self, bg=backgroundColour)
        headerFrame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(
            headerFrame,
            text=f"📐 {self.topicName}",
            font=("Arial", 18, "bold"),
            bg=backgroundColour,
            fg=accentColour
        ).pack()
        
        tk.Label(
            headerFrame,
            text="Select operation to generate Octave Code",
            font=("Arial", 10),
            bg=backgroundColour,
            fg=foregroundColour
        ).pack(pady=(5, 0))
        
        # Main content area
        contentFrame = tk.Frame(self, bg=backgroundColour)
        contentFrame.pack(padx=30, pady=10, fill="both", expand=True)
        
        # Get problem types based on the topic
        problemTypes = self.getProblemTypes()
        
        # Dropdown selection section
        selectionFrame = tk.Frame(contentFrame, bg=backgroundColour)
        selectionFrame.pack(pady=10, fill="x")
        
        tk.Label(
            selectionFrame,
            text="Problem Type:",
            font=("Arial", 11, "bold"),
            bg=backgroundColour,
            fg=foregroundColour
        ).pack(side="left", padx=(0, 10))
        
        # Create dropdown for problem types
        self.problemTypeVar = tk.StringVar()
        self.problemTypeVar.set(problemTypes[0])  # Set default value
        
        problemDropdown = ttk.Combobox(
            selectionFrame,
            textvariable=self.problemTypeVar,
            values=problemTypes,
            state="readonly",
            width=40,
            font=("Arial", 10)
        )
        problemDropdown.pack(side="left", padx=5)
        problemDropdown.bind("<<ComboboxSelected>>", self.updateInputHint)
        
        # Input area for user data
        inputFrame = tk.Frame(contentFrame, bg=backgroundColour)
        inputFrame.pack(pady=10, fill="both", expand=True)
        
        # Hint Label (Above the Text Box)
        self.hintLabel = tk.Label(
            inputFrame,
            text="Enter Matrix / Data:", # Default text
            font=("Arial", 10, "bold"),
            bg=backgroundColour,
            fg=foregroundColour, # Or accentColour for emphasis
            anchor="w",
            justify="left"
        )
        self.hintLabel.pack(fill="x", pady=(0, 5))
        
        # Scrolled text widget for input (Starts Blank)
        self.inputText = scrolledtext.ScrolledText(
            inputFrame,
            height=8,
            font=("Courier", 10),
            bg='#1e1e1e',
            fg=foregroundColour,
            insertbackground=accentColour,
            wrap="word"
        )
        self.inputText.pack(fill="both", expand=True, pady=5)
        
        # Update hint label based on default selection
        self.updateInputHint()
        
        # Buttons frame
        buttonFrame = tk.Frame(contentFrame, bg=backgroundColour)
        buttonFrame.pack(pady=15, fill="x")
        
        # Solve button
        solveButton = tk.Button(
            buttonFrame,
            text="📝 Generate Code",
            command=self.generateSolution,
            bg=accentColour,
            fg='white',
            font=("Arial", 11, "bold"),
            relief='flat',
            cursor='hand2',
            pady=10,
            padx=20
        )
        solveButton.pack(side="left", padx=5)
        
        # Clear button
        clearButton = tk.Button(
            buttonFrame,
            text="🗑️ Clear",
            command=self.clearInput,
            bg=buttonBg,
            fg=foregroundColour,
            font=("Arial", 10),
            relief='flat',
            cursor='hand2',
            pady=10,
            padx=20
        )
        clearButton.pack(side="left", padx=5)

        # Results Display Area
        resultFrame = tk.Frame(contentFrame, bg=backgroundColour)
        resultFrame.pack(pady=10, fill="both", expand=True)

        tk.Label(resultFrame, text="Generated Octave Code:", font=("Arial", 10, "bold"), 
                 bg=backgroundColour, fg=foregroundColour, anchor="w").pack(fill="x")

        self.resultText = scrolledtext.ScrolledText(
            resultFrame, height=12, font=("Courier", 10),
            bg='#1e1e1e', fg='#98c379', wrap="word"
        )
        self.resultText.pack(fill="both", expand=True)
        
        # Back button
        backButton = tk.Button(
            self,
            text="← Back to Topics",
            command=lambda: self.on_close(self.master),
            bg=backgroundColour,
            fg=accentColour,
            font=("Arial", 10),
            relief='flat',
            cursor='hand2',
            pady=8
        )
        backButton.pack(pady=10)
    
    def getProblemTypes(self):
        # Returns a list of problem types based on the selected topic
        problemMap = {
            "Matrix Properties and Manipulation": [
                "Calculate Determinant",
                "Find Matrix Inverse",
                "Calculate Trace",
                "Transpose Matrix"
            ],
            "Solving Square Linear Systems": [
                "Direct Method (Ax=b)",
                "Iterative (Gauss-Seidel)"
            ],
            "Eigenvalues and Eigenvectors": [
                "Calculate Eigenvalues"
            ],
            "Overdetermined Systems and Least Squares": [
                "Method of Least Squares"
            ],
            "Underdetermined Systems and Null Space": [
                "Find General Solution"
            ],
            "Linear Programming": [
                "Solve LP (glpk)"
            ]
        }
        return problemMap.get(self.topicName, ["Standard Operation"])
    
    def updateInputHint(self, event=None):
        # Update the label above the input box with instructions
        selected = self.problemTypeVar.get()
        
        # We DO NOT clear the text box here, just update the label
        # self.inputText.delete("1.0", "end") 
        
        hint_text = "Enter Matrix / Data:" # Default fallback
        
        if selected == "Direct Method (Ax=b)":
            hint_text = "Enter Matrix A (rows), leave a blank line, then Enter Vector b.\nExample:\n2 1\n1 3\n\n5\n8"
        elif selected == "Solve LP (glpk)":
            hint_text = "Enter c, leave blank line, Enter A, leave blank line, Enter b.\nExample (Maximize):\n40 60\n\n2 1\n1 1\n\n70\n40"
        else:
            hint_text = "Enter Matrix (space separated values, new line for each row).\nExample:\n1 2 3\n4 5 6\n7 8 9"
            
        self.hintLabel.config(text=hint_text)

    def clearInput(self):
        self.inputText.delete("1.0", "end")
        self.resultText.delete("1.0", "end")
        # Reset hint to default for current selection
        self.updateInputHint()
    
    def parse_matrix(self, text):
        # Helper to parse matrix text into list of lists
        matrix = []
        rows = text.strip().split('\n')
        for row in rows:
            if not row.strip() or row.strip().startswith("#"): continue
            try:
                matrix.append([float(x) for x in row.split()])
            except ValueError:
                pass
        return matrix

    def format_octave_matrix(self, matrix):
        # Converts [[1,2],[3,4]] to "[1 2; 3 4]" string for Octave
        row_strs = []
        for row in matrix:
            row_strs.append(" ".join(str(x) for x in row))
        return "[" + "; ".join(row_strs) + "]"

    def generateSolution(self):
        # Main logic to generate Octave Code strings
        input_str = self.inputText.get("1.0", "end")
        problem = self.problemTypeVar.get()
        octave_code = ""

        try:
            # 1. Parsing Logic
            if problem == "Direct Method (Ax=b)":
                parts = input_str.split('\n\n')
                if len(parts) < 2:
                    octave_code = "% Error: Separate A and b with a blank line in input box."
                else:
                    matrix_A = self.parse_matrix(parts[0])
                    vector_b = self.parse_matrix(parts[1])
                    
                    str_A = self.format_octave_matrix(matrix_A)
                    str_b = self.format_octave_matrix(vector_b)
                    
                    octave_code = f"""% Octave Script: Solve Ax = b
A = {str_A};
b = {str_b};

% Solve using left division operator
x = A \\ b;

disp("Solution vector x:");
disp(x);
"""

            elif problem == "Solve LP (glpk)":
                # Expecting c, A, b
                parts = input_str.split('\n\n')
                if len(parts) < 3:
                    octave_code = "% Error: Separate c, A, and b with blank lines."
                else:
                    str_c = self.format_octave_matrix(self.parse_matrix(parts[0]))
                    str_A = self.format_octave_matrix(self.parse_matrix(parts[1]))
                    str_b = self.format_octave_matrix(self.parse_matrix(parts[2]))
                    
                    octave_code = f"""% Octave Script: Linear Programming (Simplex)
c = {str_c}';  % Objective function coefficients
A = {str_A};   % Constraint matrix
b = {str_b};   % Constraint limits

% Standard bounds (x >= 0)
lb = [0; 0]; 
ub = []; 
ctype = "UU"; % Upper bounds constraints
vartype = "CC"; % Continuous variables
s = -1; % Maximize (-1) or Minimize (1)

[xmax, fmax] = glpk(c, A, b, lb, ub, ctype, vartype, s);

disp("Optimal x:");
disp(xmax);
disp("Maximum Value:");
disp(fmax);
"""

            else:
                # Standard single matrix operations
                matrix = self.parse_matrix(input_str)
                if not matrix:
                    octave_code = "% Error: Invalid Matrix Input"
                else:
                    str_A = self.format_octave_matrix(matrix)
                    
                    if problem == "Calculate Determinant":
                        octave_code = f"""% Calculate Determinant
A = {str_A};
d = det(A);
disp("Determinant:");
disp(d);
"""
                    elif problem == "Find Matrix Inverse":
                        octave_code = f"""% Calculate Inverse
A = {str_A};
if det(A) == 0
    disp("Matrix is singular, no inverse.");
else
    invA = inv(A);
    disp("Inverse Matrix:");
    disp(invA);
end
"""
                    elif problem == "Calculate Trace":
                        octave_code = f"""% Calculate Trace
A = {str_A};
t = trace(A);
disp("Trace:");
disp(t);
"""
                    elif problem == "Transpose Matrix":
                        octave_code = f"""% Transpose
A = {str_A};
AT = A';
disp("Transposed Matrix:");
disp(AT);
"""
                    elif problem == "Calculate Eigenvalues":
                        octave_code = f"""% Eigenvalues and Eigenvectors
A = {str_A};
[V, D] = eig(A);
disp("Eigenvalues (Diagonal of D):");
disp(diag(D));
disp("Eigenvectors (Columns of V):");
disp(V);
"""
                    elif problem == "Method of Least Squares":
                        octave_code = f"""% Least Squares Solution (Overdetermined)
A = {str_A};
% Note: You need a b vector. Assuming placeholder b.
b = ones(rows(A), 1); 
x = (A' * A) \\ (A' * b);
disp("Least Squares Solution x:");
disp(x);
"""
                    else:
                        octave_code = f"% Code generation for {problem} not implemented yet."

        except Exception as e:
            octave_code = f"% Error generating code: {str(e)}"

        # Display result
        self.resultText.delete("1.0", "end")
        self.resultText.insert("1.0", octave_code)
    
    def on_close(self, parent):
        # Re-enable the parent window and close this window
        parent.attributes('-disabled', False)
        self.destroy()