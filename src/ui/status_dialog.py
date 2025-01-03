import tkinter as tk
from tkinter import ttk

class StatusDialog(tk.Toplevel):
    def __init__(self, parent, task_name):
        super().__init__(parent)
        self.title(f"Update Status - {task_name}")
        self.geometry("300x200")
        self.resizable(False, False)
        
        self.result = None
        self._create_widgets()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def _create_widgets(self):
        frame = ttk.Frame(self, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            frame,
            text="Select New Status:",
            style="Header.TLabel"
        ).pack(pady=(0, 10))

        # Status selection
        self.status_var = tk.StringVar()
        for status in ["Not Started", "In Progress", "Completed"]:
            ttk.Radiobutton(
                frame,
                text=status,
                value=status,
                variable=self.status_var
            ).pack(anchor=tk.W, pady=5)
        self.status_var.set("Not Started")

        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="Update",
            style="Primary.TButton",
            command=self._on_update
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancel",
            style="Secondary.TButton",
            command=self.destroy
        ).pack(side=tk.LEFT, padx=5)

    def _on_update(self):
        self.result = self.status_var.get()
        self.destroy()
