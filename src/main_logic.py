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

    def add_task(self, task_data=None):
        """
        Add a new task to the task management system.
        Can be called from GUI or CLI.
        """
        df = pd.read_csv(self.file_name)
        next_id = df['id'].max() + 1 if not df.empty else 1

        if task_data:  # GUI mode
            name = task_data['task_name']
            category = task_data['category']
            priority = task_data['priority']
            deadline = task_data['deadline']
            dependencies = task_data['dependencies'].split(',') if task_data['dependencies'] else []
            dependencies = [d.strip() for d in dependencies if d.strip()]
        else:
            # CLI mode logic remains the same
            # ...existing code...
            return

        # Validate task name uniqueness
        if name in df['task_name'].values:
            raise ValueError("A task with this name already exists")

        # Validate dependencies
        invalid_deps = [dep for dep in dependencies if dep not in df['task_name'].values]
        if invalid_deps:
            raise ValueError(f"Invalid dependencies: {', '.join(invalid_deps)}")

        # Add dependencies to graph
        for dep in dependencies:
            self.graph.add_edge(dep, name)

        # Create task entry
        new_task = pd.DataFrame({
            'id': [next_id],
            'task_name': [name],
            'category': [category],
            'priority': [priority],
            'deadline': [deadline],
            'dependencies': [', '.join(dependencies) if dependencies else 'None'],
            'status': ['Not Started'],
            'created_at': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        })

        # Add to DataFrame and save
        df = pd.concat([df, new_task], ignore_index=True)
        df.to_csv(self.file_name, index=False)
        self.save_graph()

    def get_task_by_name(self, name):
        """
        Helper function to get task details by name.
        
        :param name: Name of the task to find
        :return: Task data as Series if found, None otherwise
        """
        df = pd.read_csv(self.file_name)
        task = df[df['task_name'] == name]
        return task.iloc[0] if not task.empty else None

    def remove_task(self, task_name):
        """
        Remove a task and update its dependencies.
        """
        df = pd.read_csv(self.file_name)
        
        if task_name not in df['task_name'].values:
            raise ValueError(f"Task '{task_name}' not found")

        # Check for dependent tasks
        dependent_tasks = []
        for _, row in df.iterrows():
            if pd.notna(row['dependencies']) and row['dependencies'] != 'None':
                deps = [d.strip() for d in str(row['dependencies']).split(',')]
                if task_name in deps:
                    dependent_tasks.append(row['task_name'])

        if dependent_tasks:
            raise ValueError(f"Cannot remove task: The following tasks depend on it: {', '.join(dependent_tasks)}")

        # Remove task and update graph
        df = df[df['task_name'] != task_name]
        if task_name in self.graph:
            self.graph.remove_node(task_name)

        # Save changes
        df.to_csv(self.file_name, index=False)
        self.save_graph()

    def update_task_status(self, task_name, new_status):
        """
        Update the status of a specific task.
        """
        df = pd.read_csv(self.file_name)
        
        if task_name not in df['task_name'].values:
            raise ValueError(f"Task '{task_name}' not found")

        valid_statuses = ["Not Started", "In Progress", "Completed"]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        # Check dependencies if marking as Completed
        if new_status == "Completed":
            task_deps = df.loc[df['task_name'] == task_name, 'dependencies'].iloc[0]
            if task_deps != 'None':
                deps = [d.strip() for d in str(task_deps).split(',')]
                incomplete_deps = []
                for dep in deps:
                    dep_status = df.loc[df['task_name'] == dep, 'status'].iloc[0]
                    if dep_status != "Completed":
                        incomplete_deps.append(dep)
                if incomplete_deps:
                    raise ValueError(f"Cannot mark as completed: Dependent tasks not completed: {', '.join(incomplete_deps)}")

        # Update status
        df.loc[df['task_name'] == task_name, 'status'] = new_status
        df.to_csv(self.file_name, index=False)

    def get_tasks(self, filters=None):
        """
        Get tasks with optional filtering.
        
        :param filters: Dictionary with filter criteria
        :return: Filtered DataFrame of tasks
        """
        df = pd.read_csv(self.file_name)
        
        if not filters:
            return df

        if 'category' in filters and filters['category']:
            df = df[df['category'].str.contains(filters['category'], case=False, na=False)]
        
        if 'min_priority' in filters and filters['min_priority']:
            df = df[df['priority'] >= filters['min_priority']]
            
        if 'status' in filters and filters['status'] != "All":
            df = df[df['status'] == filters['status']]
            
        return df

    def get_task_dependencies(self, task_name):
        """
        Get dependencies for a specific task.
        """
        df = pd.read_csv(self.file_name)
        task = df[df['task_name'] == task_name]
        
        if task.empty:
            return []
            
        deps = task.iloc[0]['dependencies']
        return [d.strip() for d in str(deps).split(',')] if deps != 'None' else []

    def view_tasks(self):
        """
        View tasks with optional filtering.
        """
        try:
            df = pd.read_csv(self.file_name)
            if df.empty:
                print("No tasks available to view.")
                return

            print("\nView Tasks:")
            print("1. View All Tasks")
            print("2. Filter by Category")
            print("3. Filter by Priority")
            print("4. Filter by Status")
            
            choice = input("Enter your choice (1-4): ").strip()
            
            def display_tasks(tasks_df):
                if tasks_df.empty:
                    print("No tasks found matching the criteria.")
                    return
                
                print("\n" + "=" * 100)
                print(f"{'ID':<5} {'Task Name':<20} {'Category':<15} {'Priority':<10} {'Status':<15} {'Deadline':<10}")
                print("=" * 100)
                
                for _, task in tasks_df.iterrows():
                    print(f"{task['id']:<5} {task['task_name']:<20} {task['category']:<15} "
                          f"{task['priority']:<10} {task['status']:<15} {task['deadline']} days")
                print("=" * 100)
            
            if choice == '1':
                display_tasks(df)
            
            elif choice == '2':
                category = input("Enter category to filter: ").strip()
                filtered_df = df[df['category'].str.contains(category, case=False, na=False)]
                display_tasks(filtered_df)
            
            elif choice == '3':
                try:
                    min_priority = int(input("Enter minimum priority (1-100): "))
                    if 1 <= min_priority <= 100:
                        filtered_df = df[df['priority'] >= min_priority]
                        display_tasks(filtered_df)
                    else:
                        print("Priority must be between 1 and 100.")
                except ValueError:
                    print("Please enter a valid number.")
            
            elif choice == '4':
                print("\nAvailable statuses:")
                print("1. Not Started")
                print("2. In Progress")
                print("3. Completed")
                status_choice = input("Enter status number (1-3): ").strip()
                
                status_map = {
                    '1': "Not Started",
                    '2': "In Progress",
                    '3': "Completed"
                }
                
                if status_choice in status_map:
                    filtered_df = df[df['status'] == status_map[status_choice]]
                    display_tasks(filtered_df)
                else:
                    print("Invalid status choice.")
            
            else:
                print("Invalid choice.")
                
        except Exception as e:
            print(f"Error viewing tasks: {e}")

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