import pandas as pd
import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class TaskManager:
    def __init__(self, file_name="tasks.csv", graph_file="dependencies.json"):
        """
        Initialize the TaskManager with file paths for tasks and dependencies.
        
        :param file_name: Path to the CSV file storing tasks
        :param graph_file: Path to the JSON file storing task dependencies
        """
        self.file_name = file_name
        self.graph_file = graph_file
        
        # Initialize the CSV file if it doesn't exist
        self.initialize_csv()
        
        # Load existing graph or create a new one
        self.graph = self.load_or_create_graph()

    def initialize_csv(self):
        """
        Create the CSV file with the required columns if it doesn't exist.
        """
        if not os.path.exists(self.file_name):
            cols = ["id", "task_name", "category", "priority", "deadline", "dependencies", "status", "created_at"]
            df = pd.DataFrame(columns=cols)
            df.to_csv(self.file_name, index=False)

    def load_or_create_graph(self):
        """
        Load existing task dependency graph or create a new one.
        
        :return: NetworkX Directed Graph of task dependencies
        """
        try:
            with open(self.graph_file, 'r') as f:
                graph_data = json.load(f)
                graph = nx.DiGraph()
                for edge in graph_data.get('edges', []):
                    graph.add_edge(edge[0], edge[1])
                return graph
        except FileNotFoundError:
            return nx.DiGraph()

    def save_graph(self):
        """
        Save the current task dependency graph to a JSON file.
        """
        graph_data = {
            'edges': list(self.graph.edges())
        }
        with open(self.graph_file, 'w') as f:
            json.dump(graph_data, f)

    def add_task(self):
        """
        Add a new task to the task management system.
        """
        # Read existing tasks
        df = pd.read_csv(self.file_name)
        
        # Determine the next ID for the task
        next_id = df['id'].max() + 1 if not df.empty else 1

        # Get task name and validate uniqueness
        name = input("Enter the task name: ").strip()
        if name in df['task_name'].values:
            print("A task with this name already exists. Please choose a unique name.")
            return

        # Get task category
        category = input("Enter the task category: ").strip()
        
        # Get priority with validation
        while True:
            try:
                priority = int(input("Enter the priority (1-100): "))
                if 1 <= priority <= 100:
                    break
                else:
                    print("Priority must be between 1 and 100.")
            except ValueError:
                print("Please enter a valid integer.")

        # Get deadline with validation
        while True:
            try:
                deadline = int(input("Enter the deadline in days: "))
                if deadline > 0:
                    break
                else:
                    print("Deadline must be a positive number.")
            except ValueError:
                print("Please enter a valid integer.")

        # Handle dependencies
        dependencies_input = input("Enter the dependencies (comma-separated task names, or press Enter if none): ").strip()
        dependencies = [dep.strip() for dep in dependencies_input.split(',') if dep.strip()] if dependencies_input else []

        # Validate dependencies
        invalid_dependencies = [dep for dep in dependencies if dep not in df['task_name'].values]
        if invalid_dependencies:
            print(f"Warning: The following dependencies do not exist: {invalid_dependencies}")
            continue_add = input("Do you want to continue? (y/n): ").strip().lower()
            if continue_add != 'y':
                return

        # Add dependencies to graph
        for dependency in dependencies:
            self.graph.add_edge(dependency, name)

        # Prepare task data
        task_data = pd.DataFrame({
            "id": [next_id],
            "task_name": [name],
            "category": [category],
            "priority": [priority],
            "deadline": [deadline],
            "dependencies": [', '.join(dependencies) if dependencies else 'None'],
            "status": ["Not Started"],
            "created_at": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        })

        # Append to CSV (using pd.concat instead of deprecated append method)
        df = pd.concat([df, task_data], ignore_index=True)
        df.to_csv(self.file_name, index=False)

        # Save graph
        self.save_graph()
        print("Task added successfully!")

    def remove_task(self):
        """
        Remove a task from the task management system.
        """
        # Read current tasks
        df = pd.read_csv(self.file_name)
        
        # Display current tasks
        print("\nCurrent Tasks:")
        print(df.to_string(index=False))
        
        # Get task name to remove
        name = input("\nEnter the name of the task to remove: ").strip()
        
        # Check if task exists
        if name not in df['task_name'].values:
            print(f"Task '{name}' not found in the list.")
            return
        
        # Remove task from DataFrame
        df = df[df['task_name'] != name]
        df.to_csv(self.file_name, index=False)
        
        # Remove task from graph
        if name in self.graph:
            self.graph.remove_node(name)
        self.save_graph()
        
        print(f"Task '{name}' has been removed successfully.")
        
        # Display updated tasks
        print("\nUpdated Tasks:")
        print(df.to_string(index=False))

    def update_task_status(self):
        """
        Update the status of a specific task.
        """
        df = pd.read_csv(self.file_name)
        
        # Display current tasks
        print("\nCurrent Tasks:")
        print(df.to_string(index=False))
        
        # Select task to update
        name = input("\nEnter the name of the task to update: ").strip()
        
        # Check if task exists
        if name not in df['task_name'].values:
            print(f"Task '{name}' not found in the list.")
            return
        
        # Status selection menu
        print("\nSelect new status:")
        print("1. Not Started")
        print("2. In Progress")
        print("3. Completed")
        
        status_choice = input("Enter your choice (1-3): ").strip()
        status_map = {
            '1': "Not Started",
            '2': "In Progress",
            '3': "Completed"
        }
        
        if status_choice not in status_map:
            print("Invalid choice. Status not updated.")
            return
        
        # Update status in DataFrame
        df.loc[df['task_name'] == name, 'status'] = status_map[status_choice]
        df.to_csv(self.file_name, index=False)
        
        print(f"Status of task '{name}' updated to {status_map[status_choice]}.")

    def view_tasks(self):
        """
        View tasks with optional filtering.
        """
        df = pd.read_csv(self.file_name)
        
        # Filtering options menu
        print("\nView Tasks:")
        print("1. View All Tasks")
        print("2. Filter by Category")
        print("3. Filter by Priority")
        print("4. Filter by Status")
        
        # Take user choice
        choice = input("Enter your choice (1-4): ").strip()
        
        # Different view options based on user choice
        if choice == '1':
            print(df.to_string(index=False))
        elif choice == '2':
            category = input("Enter category to filter: ").strip()
            filtered_df = df[df['category'].str.contains(category, case=False)]
            print(filtered_df.to_string(index=False) if not filtered_df.empty else "No tasks found.")
        elif choice == '3':
            while True:
                try:
                    min_priority = int(input("Enter minimum priority: "))
                    filtered_df = df[df['priority'] >= min_priority]
                    print(filtered_df.to_string(index=False) if not filtered_df.empty else "No tasks found.")
                    break
                except ValueError:
                    print("Please enter a valid integer.")
        elif choice == '4':
            status = input("Enter status to filter (Not Started/In Progress/Completed): ").strip()
            filtered_df = df[df['status'] == status]
            print(filtered_df.to_string(index=False) if not filtered_df.empty else "No tasks found.")
        else:
            print("Invalid choice.")

    def view_overdue_tasks(self):
        """
        View tasks that are past their deadline.
        """
        df = pd.read_csv(self.file_name)
        
        # Get current date
        current_date = datetime.now()
        
        # Calculate overdue tasks
        df['deadline_date'] = pd.to_datetime(current_date) - pd.to_timedelta(df['deadline'], unit='D')
        overdue_tasks = df[df['deadline_date'] > current_date]
        
        if overdue_tasks.empty:
            print("No overdue tasks!")
        else:
            print("\nOverdue Tasks:")
            print(overdue_tasks.to_string(index=False))

    def visualize_dependencies(self):
        """
        Create a visual representation of task dependencies.
        """
        if not self.graph.nodes():
            print("No dependencies to visualize.")
            return
        
        # Create a matplotlib figure
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, 
                node_color='lightblue', 
                node_size=3000, 
                font_size=10, 
                font_weight='bold', 
                arrows=True)
        plt.title("Task Dependencies")
        plt.show()

    def export_tasks(self):
        """
        Export tasks to a CSV file.
        """
        export_file = input("Enter the export file name (e.g., tasks_backup.csv): ").strip()
        
        df = pd.read_csv(self.file_name)
        df.to_csv(export_file, index=False)
        
        print(f"Tasks exported to {export_file} successfully!")

    def main_menu(self):
        """
        Main menu for the task management system.
        """
        while True:
            print("\n--- Task Management System ---")
            print("1. Add Task")
            print("2. Remove Task")
            print("3. Update Task Status")
            print("4. View Tasks")
            print("5. View Overdue Tasks")
            print("6. Visualize Dependencies")
            print("7. Export Tasks")
            print("8. Exit")
            
            # Take user choice
            choice = input("Enter your choice (1-8): ").strip()
            
            # Perform actions based on user choice
            try:
                if choice == '1':
                    self.add_task()
                elif choice == '2':
                    self.remove_task()
                elif choice == '3':
                    self.update_task_status()
                elif choice == '4':
                    self.view_tasks()
                elif choice == '5':
                    self.view_overdue_tasks()
                elif choice == '6':
                    self.visualize_dependencies()
                elif choice == '7':
                    self.export_tasks()
                elif choice == '8':
                    print("Exiting Task Management System. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")

def main():
    """
    Initialize and start the task management application.
    """
    task_manager = TaskManager()
    task_manager.main_menu()

if __name__ == "__main__":
    main()