import tkinter as tk

class CalculatorLogic:
    """Handles the mathematical state and calculations behind the calculator UI."""
    
    def __init__(self):
        """Initializes an empty expression state."""
        self.expression = ""

    def append(self, char: str) -> str:
        """Appends a character to the current expression."""
        if self.expression == "Error":
            self.expression = ""
        self.expression += str(char)
        return self.expression

    def clear(self) -> str:
        """Clears the mathematical expression entirely."""
        self.expression = ""
        return self.expression

    def evaluate(self) -> str:
        """Safely evaluates the expression using Python's built-in eval()."""
        try:
            # Note: eval() is generally discouraged for unknown inputs. 
            # In a local, button-driven GUI context, the inputs are controlled.
            result = str(eval(self.expression))
            self.expression = result
            return self.expression
        except ZeroDivisionError:
            self.expression = "Error"
            return "Error"
        except Exception:
            self.expression = "Error"
            return "Error"

class CalculatorGUI:
    """Responsible for building and interacting with the Tkinter UI layout."""

    # --- Soft Pastel Theme Configuration ---
    BG_COLOR = "#F4F1DE"       # Soft pastel eggshell background
    BTN_FG = "#5C5C5C"         # Soft dark grey text
    BTN_ACTIVE_BG = "#EFEFEF"  # Slightly darker white/grey for click effect
    BTN_ACTIVE_FG = "#5C5C5C"  
    
    ACCENT_NUM = "#FFFFFF"     # Clean white for numbers
    ACCENT_OP = "#FFB7B2"      # Pastel Pink for operators
    ACCENT_EQ = "#C7CEEA"      # Pastel Violet for Equals
    ACCENT_CLEAR = "#E2F0CB"   # Pastel lime/mint for Clear
    DISPLAY_FG = "#5C5C5C"     # Soft dark grey text for display output

    FONT_MAIN = ('Segoe UI', 16, 'bold')
    FONT_DISPLAY = ('Segoe UI', 32, 'bold')

    def __init__(self, master: tk.Tk, logic: CalculatorLogic):
        self.master = master
        self.logic = logic
        
        # Setup master window configuration
        self.master.title("Pastel Calculator")
        self.master.geometry("340x440")
        self.master.resizable(False, False)
        self.master.configure(bg=self.BG_COLOR)

        self.input_text = tk.StringVar()
        
        self.setup_ui()
        self.create_buttons()

    def setup_ui(self):
        """Configures the input display frame and the button container frame."""
        # Top Display Frame
        self.input_frame = tk.Frame(self.master, width=340, height=80, bd=0, bg=self.BG_COLOR)
        self.input_frame.pack(side=tk.TOP, fill=tk.BOTH)

        # Entry Widget (The Screen)
        self.input_field = tk.Entry(self.input_frame, font=self.FONT_DISPLAY, textvariable=self.input_text, 
                                    width=50, bg=self.BG_COLOR, fg=self.DISPLAY_FG, bd=0, 
                                    justify=tk.RIGHT, insertbackground=self.DISPLAY_FG)
        self.input_field.grid(row=0, column=0)
        self.input_field.pack(ipady=20, padx=15, pady=10)

        # Bottom Buttons Frame
        self.btns_frame = tk.Frame(self.master, width=340, height=360, bg=self.BG_COLOR)
        self.btns_frame.pack(fill=tk.BOTH, expand=True)

        # Responsive grid weights
        for i in range(5):
            self.btns_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.btns_frame.grid_columnconfigure(i, weight=1)

    def _create_button(self, text: str, row: int, col: int, command, width: int = 5, col_span: int = 1, bg_color: str = "#FFFFFF"):
        """Helper to cleanly instantiate grid buttons."""
        btn = tk.Button(self.btns_frame, text=text, fg=self.BTN_FG, width=width, height=2, bd=0,
                        bg=bg_color, cursor="hand2", font=self.FONT_MAIN, command=command, 
                        activebackground=self.BTN_ACTIVE_BG, activeforeground=self.BTN_ACTIVE_FG)
        btn.grid(row=row, column=col, columnspan=col_span, padx=3, pady=3, sticky="nsew")
        return btn

    def create_buttons(self):
        """Maps specific buttons onto the visual grid."""
        # Row 1
        self._create_button("CLEAR", 0, 0, self.on_clear, width=16, col_span=3, bg_color=self.ACCENT_CLEAR)
        self._create_button("÷", 0, 3, lambda: self.on_click("/"), bg_color=self.ACCENT_OP)

        # Row 2
        self._create_button("7", 1, 0, lambda: self.on_click("7"), bg_color=self.ACCENT_NUM)
        self._create_button("8", 1, 1, lambda: self.on_click("8"), bg_color=self.ACCENT_NUM)
        self._create_button("9", 1, 2, lambda: self.on_click("9"), bg_color=self.ACCENT_NUM)
        self._create_button("×", 1, 3, lambda: self.on_click("*"), bg_color=self.ACCENT_OP)

        # Row 3
        self._create_button("4", 2, 0, lambda: self.on_click("4"), bg_color=self.ACCENT_NUM)
        self._create_button("5", 2, 1, lambda: self.on_click("5"), bg_color=self.ACCENT_NUM)
        self._create_button("6", 2, 2, lambda: self.on_click("6"), bg_color=self.ACCENT_NUM)
        self._create_button("-", 2, 3, lambda: self.on_click("-"), bg_color=self.ACCENT_OP)

        # Row 4
        self._create_button("1", 3, 0, lambda: self.on_click("1"), bg_color=self.ACCENT_NUM)
        self._create_button("2", 3, 1, lambda: self.on_click("2"), bg_color=self.ACCENT_NUM)
        self._create_button("3", 3, 2, lambda: self.on_click("3"), bg_color=self.ACCENT_NUM)
        self._create_button("+", 3, 3, lambda: self.on_click("+"), bg_color=self.ACCENT_OP)

        # Row 5
        self._create_button("0", 4, 0, lambda: self.on_click("0"), width=16, col_span=2, bg_color=self.ACCENT_NUM)
        self._create_button(".", 4, 2, lambda: self.on_click("."), bg_color=self.ACCENT_NUM)
        self._create_button("=", 4, 3, self.on_evaluate, bg_color=self.ACCENT_EQ)

    # UI Interaction Handlers
    def on_click(self, char: str):
        """Triggers appending a character and updates display."""
        new_expr = self.logic.append(char)
        self.input_text.set(new_expr)

    def on_clear(self):
        """Triggers clear logic and resets display."""
        new_expr = self.logic.clear()
        self.input_text.set(new_expr)

    def on_evaluate(self):
        """Triggers evaluate logic and updates display."""
        new_expr = self.logic.evaluate()
        self.input_text.set(new_expr)

if __name__ == "__main__":
    root = tk.Tk()
    logic_layer = CalculatorLogic()
    app = CalculatorGUI(root, logic_layer)
    root.mainloop()
