import tkinter as tk
from tkinter import ttk
from .style import apply_style

class TaskDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Task")
        self.geometry("400x500")
        apply_style(self)
        
        self.result = None
        self._create_widgets()
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        self.wait_window()

    def _create_widgets(self):
        # Task name
        ttk.Label(self, text="Task Name:").pack(pady=5)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(fill=tk.X, padx=20)

        # Category
        ttk.Label(self, text="Category:").pack(pady=5)
        self.category_entry = ttk.Entry(self)
        self.category_entry.pack(fill=tk.X, padx=20)

        # Priority
        ttk.Label(self, text="Priority (1-100):").pack(pady=5)
        self.priority_spinbox = ttk.Spinbox(self, from_=1, to=100)
        self.priority_spinbox.pack(fill=tk.X, padx=20)

        # Deadline
        ttk.Label(self, text="Deadline (days):").pack(pady=5)
        self.deadline_spinbox = ttk.Spinbox(self, from_=1, to=365)
        self.deadline_spinbox.pack(fill=tk.X, padx=20)

        # Dependencies
        ttk.Label(self, text="Dependencies (comma-separated):").pack(pady=5)
        self.dependencies_entry = ttk.Entry(self)
        self.dependencies_entry.pack(fill=tk.X, padx=20)

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _save(self):
        self.result = {
            "task_name": self.name_entry.get(),
            "category": self.category_entry.get(),
            "priority": int(self.priority_spinbox.get()),
            "deadline": int(self.deadline_spinbox.get()),
            "dependencies": self.dependencies_entry.get()
        }
        self.destroy()
