import tkinter as tk
from tkinter import ttk
from .task_dialog import TaskDialog
from .style import apply_style

class MainWindow(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.title("Task Management System")
        self.geometry("800x600")
        apply_style(self)
        self._create_widgets()

    def _create_widgets(self):
        # Create main menu
        self.menu_frame = ttk.Frame(self)
        self.menu_frame.pack(pady=10)

        buttons = [
            ("Add Task", self._add_task),
            ("View Tasks", self._view_tasks),
            ("Update Task", self._update_task),
            ("Remove Task", self._remove_task),
            ("View Dependencies", self._view_dependencies)
        ]

        for text, command in buttons:
            ttk.Button(self.menu_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)

        # Task list
        self.task_frame = ttk.Frame(self)
        self.task_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._refresh_task_list()

    def _refresh_task_list(self):
        # Clear existing list
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        # Create headers
        headers = ["Task Name", "Category", "Priority", "Deadline", "Status"]
        for i, header in enumerate(headers):
            ttk.Label(self.task_frame, text=header, font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)

        # Load tasks
        tasks_df = self.task_manager.get_tasks()
        for i, (_, task) in enumerate(tasks_df.iterrows(), start=1):
            ttk.Label(self.task_frame, text=task['task_name']).grid(row=i, column=0, padx=5, pady=2)
            ttk.Label(self.task_frame, text=task['category']).grid(row=i, column=1, padx=5, pady=2)
            ttk.Label(self.task_frame, text=str(task['priority'])).grid(row=i, column=2, padx=5, pady=2)
            ttk.Label(self.task_frame, text=str(task['deadline'])).grid(row=i, column=3, padx=5, pady=2)
            ttk.Label(self.task_frame, text=task['status']).grid(row=i, column=4, padx=5, pady=2)

    def _add_task(self):
        dialog = TaskDialog(self)
        if dialog.result:
            self.task_manager.add_task(dialog.result)
            self._refresh_task_list()

    def _view_tasks(self):
        self._refresh_task_list()

    def _update_task(self):
        selected_task = self._get_selected_task()
        if selected_task:
            dialog = TaskDialog(self, task=selected_task)
            if dialog.result:
                self.task_manager.update_task(selected_task['task_name'], dialog.result)
                self._refresh_task_list()

    def _remove_task(self):
        selected_task = self._get_selected_task()
        if selected_task:
            if tk.messagebox.askyesno("Confirm", f"Delete task '{selected_task['task_name']}'?"):
                self.task_manager.remove_task(selected_task['task_name'])
                self._refresh_task_list()

    def _view_dependencies(self):
        self.task_manager.visualize_dependencies()

    def _get_selected_task(self):
        # Implement task selection logic
        pass
