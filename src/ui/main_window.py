import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from .task_dialog import TaskDialog
from .status_dialog import StatusDialog
from .style import apply_style, ThemeManager, THEMES

class MainWindow(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.title("Task Management System")
        self.geometry("1200x700")
        
        # Initialize theme manager
        self.theme_manager = ThemeManager(self)
        self.style, self.colors = self.theme_manager.apply_theme()
        
        self._create_widgets()
        
        # Set initial theme
        self._change_theme()

    def _create_widgets(self):
        # Create main container with padding
        self.main_container = ttk.Frame(self, padding="10")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create left and right panes
        self.left_pane = ttk.Frame(self.main_container)
        self.left_pane.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_pane = ttk.Frame(self.main_container)
        self.right_pane.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        # Create widgets in left pane
        self._create_toolbar(self.left_pane)
        self._create_filter_frame(self.left_pane)
        self._create_task_list(self.left_pane)

        # Create widgets in right pane
        self._create_task_details(self.right_pane)

        # Initial refresh
        self._refresh_task_list()

    def _create_toolbar(self, parent):
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        # Main buttons
        buttons = [
            ("Add Task", "Primary.TButton", self._add_task),
            ("Remove Task", "Secondary.TButton", self._remove_task),
            ("Update Status", "Success.TButton", self._update_task_status),
            ("View Dependencies", "Primary.TButton", self._view_dependencies),
            ("Export Tasks", "Secondary.TButton", self._export_tasks)
        ]

        for text, style, command in buttons:
            ttk.Button(
                toolbar, 
                text=text,
                style=style,
                command=command
            ).pack(side=tk.LEFT, padx=5)

        # Theme selector
        theme_frame = ttk.Frame(toolbar)
        theme_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(
            theme_frame,
            text="Theme:",
            style="Body.TLabel"
        ).pack(side=tk.LEFT, padx=5)
        
        self.theme_var = tk.StringVar(value="light")
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=list(THEMES.keys()),
            state="readonly",
            width=10
        )
        theme_combo.pack(side=tk.LEFT)
        theme_combo.bind('<<ComboboxSelected>>', self._change_theme)

    def _change_theme(self, event=None):
        """
        Change the application theme and update all widgets
        """
        theme = self.theme_var.get() if hasattr(self, 'theme_var') else 'light'
        self.style, self.colors = self.theme_manager.apply_theme(theme)
        
        # Update all frames backgrounds
        for widget in self.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.configure(style='TFrame')
        
        # Refresh the task list to apply new styles
        if hasattr(self, 'tree'):
            self._refresh_task_list()

    def _create_filter_frame(self, parent):
        filter_frame = ttk.LabelFrame(parent, text="Filters", padding="10")
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        # Create filter controls grid
        filters_grid = ttk.Frame(filter_frame)
        filters_grid.pack(fill=tk.X, padx=5, pady=5)

        # Category filter
        ttk.Label(filters_grid, text="Category:").grid(row=0, column=0, padx=5)
        self.category_var = tk.StringVar()
        ttk.Entry(filters_grid, textvariable=self.category_var).grid(row=0, column=1, padx=5)

        # Priority filter
        ttk.Label(filters_grid, text="Min Priority:").grid(row=0, column=2, padx=5)
        self.priority_var = tk.StringVar(value="0")
        ttk.Spinbox(
            filters_grid, from_=0, to=100,
            textvariable=self.priority_var, width=5
        ).grid(row=0, column=3, padx=5)

        # Status filter
        ttk.Label(filters_grid, text="Status:").grid(row=0, column=4, padx=5)
        self.status_var = tk.StringVar(value="All")
        ttk.Combobox(
            filters_grid,
            textvariable=self.status_var,
            values=["All", "Not Started", "In Progress", "Completed"],
            state="readonly",
            width=15
        ).grid(row=0, column=5, padx=5)

        # Apply filters button
        ttk.Button(
            filters_grid,
            text="Apply Filters",
            style="Primary.TButton",
            command=self._apply_filters
        ).grid(row=0, column=6, padx=5)

    def _create_task_list(self, parent):
        # Task list container
        list_frame = ttk.LabelFrame(parent, text="Tasks", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Create treeview with scrollbar
        columns = ("ID", "Task Name", "Category", "Priority", "Deadline", "Status")
        self.tree = ttk.Treeview(
            list_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_tasks(c))
            width = 100 if col != "Task Name" else 200
            self.tree.column(col, width=width)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        x_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout for scrollable tree
        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Configure grid weights
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self._on_task_select)

    def _create_task_details(self, parent):
        details_frame = ttk.LabelFrame(parent, text="Task Details", padding="10")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Details view
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, width=40, height=20)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)

    def _apply_filters(self):
        """
        Apply selected filters and refresh the task list
        """
        try:
            # Reset any previous filter errors
            self.category_var.set(self.category_var.get().strip())
            
            # Validate priority input
            try:
                priority = int(self.priority_var.get() or 0)
                if priority < 0 or priority > 100:
                    messagebox.showwarning("Invalid Priority", 
                                         "Priority must be between 0 and 100")
                    self.priority_var.set("0")
                    return
            except ValueError:
                messagebox.showwarning("Invalid Priority", 
                                     "Priority must be a number")
                self.priority_var.set("0")
                return

            # Refresh the task list with current filters
            self._refresh_task_list()
            
        except Exception as e:
            messagebox.showerror("Filter Error", f"Error applying filters: {e}")

    def _refresh_task_list(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Get filtered tasks
            filters = {
                'category': self.category_var.get(),
                'min_priority': int(self.priority_var.get() or 0),
                'status': self.status_var.get()
            }
            df = self.task_manager.get_tasks(filters)

            # Insert tasks into tree
            for _, task in df.iterrows():
                self.tree.insert("", tk.END, values=(
                    task['id'],
                    task['task_name'],
                    task['category'],
                    task['priority'],
                    f"{task['deadline']} days",
                    task['status']
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading tasks: {e}")

    def _on_task_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        # Get selected task details
        task_name = self.tree.item(selected_items[0])['values'][1]
        task = self.task_manager.get_task_by_name(task_name)
        
        if task is not None:
            # Update details view
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete(1.0, tk.END)
            
            details = f"""Task Name: {task['task_name']}
Category: {task['category']}
Priority: {task['priority']}
Deadline: {task['deadline']} days
Status: {task['status']}
Dependencies: {task['dependencies']}
Created: {task['created_at']}"""
            
            self.details_text.insert(tk.END, details)
            self.details_text.config(state=tk.DISABLED)

    def _add_task(self):
        dialog = TaskDialog(self)
        if dialog.result:
            try:
                self.task_manager.add_task(dialog.result)
                self._refresh_task_list()
                messagebox.showinfo("Success", "Task added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding task: {e}")

    def _remove_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to remove.")
            return

        task_name = self.tree.item(selected_item)['values'][1]  # Get task name from selected row
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove task '{task_name}'?"):
            try:
                self.task_manager.remove_task(task_name)
                self._refresh_task_list()
                messagebox.showinfo("Success", "Task removed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error removing task: {e}")

    def _update_task_status(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to update.")
            return

        task_name = self.tree.item(selected_item)['values'][1]
        status_dialog = StatusDialog(self, task_name)
        if status_dialog.result:
            try:
                self.task_manager.update_task_status(task_name, status_dialog.result)
                self._refresh_task_list()
                messagebox.showinfo("Success", "Task status updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating task status: {e}")

    def _view_dependencies(self):
        self.task_manager.visualize_dependencies()

    def _export_tasks(self):
        """
        Export tasks to a CSV file using file dialog
        """
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export Tasks"
            )
            if filename:
                # Get all tasks without filters
                df = pd.read_csv(self.task_manager.file_name)
                df.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Tasks exported successfully to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting tasks: {e}")
