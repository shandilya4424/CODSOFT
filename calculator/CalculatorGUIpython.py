import customtkinter as ctk

# Initialize appearance and theme
ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("blue")

class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧮 Simple Calculator")
        self.geometry("350x500")
        self.resizable(False, False)

        self.expression = ""

        # Display screen
        self.display = ctk.CTkEntry(self, font=("Arial", 28), justify="right", width=300)
        self.display.pack(pady=20, padx=10)

        # Button layout
        self.create_buttons()

        # Bind keyboard keys
        self.bind_all("<Key>", self.handle_keypress)

    def create_buttons(self):
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        # Button layout grid
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "=", "+"]
        ]

        for row_idx, row in enumerate(buttons):
            for col_idx, btn_text in enumerate(row):
                btn = ctk.CTkButton(
                    button_frame, text=btn_text, width=60, height=60, font=("Arial", 18),
                    command=lambda val=btn_text: self.on_button_click(val)
                )
                btn.grid(row=row_idx, column=col_idx, padx=5, pady=5)

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
        elif char == "=":
            try:
                result = str(eval(self.expression))
                self.expression = result
            except:
                self.expression = "Error"
        else:
            self.expression += char

        self.update_display()

    def update_display(self):
        self.display.delete(0, ctk.END)
        self.display.insert(0, self.expression)

    def handle_keypress(self, event):
        key = event.char
        if key in "0123456789+-*/.":
            self.expression += key
        elif event.keysym == "Return":
            try:
                self.expression = str(eval(self.expression))
            except:
                self.expression = "Error"
        elif event.keysym in ["BackSpace", "Delete"]:
            self.expression = self.expression[:-1]
        elif event.char.lower() == "c":
            self.expression = ""

        self.update_display()

# 🏁 Run the calculator
if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
