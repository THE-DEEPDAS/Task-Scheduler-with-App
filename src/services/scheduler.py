
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
from models.task import Task, TaskType

class Scheduler:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.working_hours = {
            'start': '09:00',
            'end': '17:00',
            'break_duration': 60  # minutes
        }

    def get_available_slots(self, date: datetime, duration: int = 60) -> List[datetime]:
        """Get available time slots for a specific date."""
        booked_slots = self.get_booked_slots(date)
        all_slots = self.generate_day_slots(date)
        return [slot for slot in all_slots if not self._is_slot_booked(slot, duration, booked_slots)]

    def book_appointment(self, client: str, start_time: datetime, 
                       duration: int, service_type: str) -> Task:
        """Book a new appointment."""
        if not self._is_slot_available(start_time, duration):
            raise ValueError("Time slot not available")

        task_data = {
            "task_name": f"Appointment - {client}",
            "category": service_type,
            "priority": 1,
            "deadline": 0,
            "task_type": TaskType.APPOINTMENT,
            "start_time": start_time,
            "duration": duration,
            "client": client,
            "payment_status": "pending"
        }
        
        return self.task_manager.add_task(task_data)

    def _is_slot_booked(self, slot: datetime, duration: int, 
                       booked_slots: List[Dict]) -> bool:
        """Check if a time slot is already booked."""
        slot_end = slot + timedelta(minutes=duration)
        for booked in booked_slots:
            booked_end = booked['start'] + timedelta(minutes=booked['duration'])
            if (slot < booked_end and slot_end > booked['start']):
                return True
        return False