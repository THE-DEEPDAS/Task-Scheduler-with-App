from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum

class TaskType(Enum):
    APPOINTMENT = "appointment"
    BREAK = "break"
    MEETING = "meeting"
    REGULAR = "regular"

class Task:
    def __init__(self, id: int, task_name: str, category: str, priority: int,
                 deadline: int, dependencies: List[str] = None,
                 status: str = "Not Started", task_type: TaskType = TaskType.REGULAR,
                 start_time: datetime = None, duration: int = 60,
                 assigned_to: str = None, client: str = None,
                 payment_status: str = None, deposit_amount: float = 0.0):
        self.id = id
        self.task_name = task_name
        self.category = category
        self.priority = priority
        self.deadline = deadline
        self.dependencies = dependencies or []
        self.status = status
        self.created_at = datetime.now()
        self.task_type = task_type
        self.start_time = start_time
        self.duration = duration  # in minutes
        self.assigned_to = assigned_to
        self.client = client
        self.payment_status = payment_status
        self.deposit_amount = deposit_amount
        self.notifications_sent = []
        self.waitlist = []

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "task_name": self.task_name,
            "category": self.category,
            "priority": self.priority,
            "deadline": self.deadline,
            "dependencies": ", ".join(self.dependencies) if self.dependencies else "None",
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "task_type": self.task_type.value,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "duration": self.duration,
            "assigned_to": self.assigned_to,
            "client": self.client,
            "payment_status": self.payment_status,
            "deposit_amount": self.deposit_amount,
            "waitlist": self.waitlist
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
