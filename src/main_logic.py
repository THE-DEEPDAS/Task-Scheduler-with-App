import pandas as pd
import json
import os
import networkx as nx
from models.task import Task
from utils.graph_utils import create_dependency_graph, visualize_graph
from config.settings import TASKS_FILE, DEPENDENCIES_FILE
from datetime import datetime

class TaskManager:
    def __init__(self, file_name=TASKS_FILE, graph_file=DEPENDENCIES_FILE):
        self.file_name = file_name
        self.graph_file = graph_file
        self._initialize_csv()
        self.graph = self._load_or_create_graph()

    def _initialize_csv(self):
        """
        Create the CSV file with the required columns if it doesn't exist.
        """
        if not os.path.exists(self.file_name):
            cols = ["id", "task_name", "category", "priority", "deadline", "dependencies", "status", "created_at"]
            df = pd.DataFrame(columns=cols)
            df.to_csv(self.file_name, index=False)

    def _load_or_create_graph(self):
        """
        Load existing task dependency graph or create a new one.
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

    def add_task(self, task_data):
        """
        Add a new task using the GUI data.
        """
        df = pd.read_csv(self.file_name)
        next_id = df['id'].max() + 1 if not df.empty else 1
        
        # Create new task
        task = Task(
            id=next_id,
            task_name=task_data['task_name'],
            category=task_data['category'],
            priority=task_data['priority'],
            deadline=task_data['deadline'],
            dependencies=task_data['dependencies'].split(',') if task_data['dependencies'] else [],
            status="Not Started"
        )
        
        # Add to DataFrame
        task_dict = task.to_dict()
        df = pd.concat([df, pd.DataFrame([task_dict])], ignore_index=True)
        df.to_csv(self.file_name, index=False)
        
        # Update dependencies graph
        if task.dependencies:
            for dep in task.dependencies:
                self.graph.add_edge(dep.strip(), task.task_name)
            self._save_graph()

    def get_tasks(self):
        """
        Return the current tasks DataFrame.
        """
        return pd.read_csv(self.file_name)

    def update_task(self, task_name, new_data):
        """
        Update an existing task with new data.
        """
        df = pd.read_csv(self.file_name)
        task_idx = df[df['task_name'] == task_name].index[0]
        for key, value in new_data.items():
            df.at[task_idx, key] = value
        df.to_csv(self.file_name, index=False)

    def remove_task(self, task_name):
        """
        Remove a task by name.
        """
        df = pd.read_csv(self.file_name)
        df = df[df['task_name'] != task_name]
        df.to_csv(self.file_name, index=False)
        
        if task_name in self.graph:
            self.graph.remove_node(task_name)
            self._save_graph()

    def _save_graph(self):
        """
        Save the current task dependency graph to a JSON file.
        """
        graph_data = {
            'edges': list(self.graph.edges())
        }
        with open(self.graph_file, 'w') as f:
            json.dump(graph_data, f)

    def visualize_dependencies(self):
        """
        Create a visual representation of task dependencies.
        """
        if not self.graph.nodes():
            print("No dependencies to visualize.")
            return
        
        visualize_graph(self.graph)

    # ...existing code for other methods...
