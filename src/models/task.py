from datetime import datetime
from typing import List, Optional

class Task:
    def __init__(self, id: int, task_name: str, category: str, priority: int, 
                 deadline: int, dependencies: List[str] = None, 
                 status: str = "Not Started"):
        self.id = id
        self.task_name = task_name
        self.category = category
        self.priority = priority
        self.deadline = deadline
        self.dependencies = dependencies or []
        self.status = status
        self.created_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_name": self.task_name,
            "category": self.category,
            "priority": self.priority,
            "deadline": self.deadline,
            "dependencies": ", ".join(self.dependencies) if self.dependencies else "None",
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        dependencies = (data.get('dependencies', "None").split(", ") 
                      if data.get('dependencies') != "None" else [])
        return cls(
            id=data['id'],
            task_name=data['task_name'],
            category=data['category'],
            priority=data['priority'],
            deadline=data['deadline'],
            dependencies=dependencies,
            status=data['status']
        )
