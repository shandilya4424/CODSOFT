import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class EditDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Edit Task", current_text=""):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        self.updated_text = None

        ctk.CTkLabel(self, text="Update your task:").pack(pady=10)
        self.entry = ctk.CTkEntry(self, width=250)
        self.entry.insert(0, current_text)
        self.entry.pack(pady=5)

        ctk.CTkButton(self, text="Save", command=self.save).pack(pady=10)

        self.entry.focus_set()
        self.grab_set()

    def save(self):
        self.updated_text = self.entry.get()
        self.destroy()


class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("To-Do List App")
        self.geometry("500x550")
        self.tasks = []

        ctk.CTkLabel(self, text="My Task List", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

        self.task_frame = ctk.CTkScrollableFrame(self, width=450, height=350)
        self.task_frame.pack(pady=10)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Add", command=self.add_task_popup, width=100).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Edit", command=self.edit_task, width=100).grid(row=0, column=1, padx=10)
        ctk.CTkButton(button_frame, text="Delete", command=self.delete_task, width=100).grid(row=0, column=2, padx=10)

        
        self.task_widgets = []

    
    def add_task_popup(self):
        task = ctk.CTkInputDialog(title="Add Task", text="Enter your task:").get_input()
        if task:
            self.create_task(task)

    def create_task(self, task_text):
        task_var = ctk.BooleanVar(value=False)
        frame = ctk.CTkFrame(self.task_frame)
        frame.pack(fill="x", pady=3, padx=5)

        checkbox = ctk.CTkCheckBox(frame, text=task_text, variable=task_var, font=ctk.CTkFont(size=14),
                                   command=lambda: self.toggle_task(task_var, checkbox))
        checkbox.pack(side="left", anchor="w")

        self.task_widgets.append({"frame": frame, "checkbox": checkbox, "var": task_var})

    def toggle_task(self, var, checkbox):
        if var.get():
            checkbox.configure(font=ctk.CTkFont(size=14, slant="italic"), text_color="gray")
        else:
            checkbox.configure(font=ctk.CTkFont(size=14), text_color="black")

    def get_selected_task(self):
        for task in self.task_widgets:
            if task["var"].get():
                return task
        return None
    
    def delete_task(self):
        selected = self.get_selected_task()
        if selected:
            selected["frame"].destroy()
            self.task_widgets.remove(selected)
        else:
            messagebox.showinfo("Delete Task", "Please check the task to delete it.")

    def edit_task(self):
        selected = self.get_selected_task()
        if selected:
            current_text = selected["checkbox"].cget("text")
            dialog = EditDialog(self, current_text=current_text)
            self.wait_window(dialog)

            if dialog.updated_text:
                selected["checkbox"].configure(text=dialog.updated_text)
        else:
            messagebox.showinfo("Edit Task", "Please check the task to edit it.")


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
