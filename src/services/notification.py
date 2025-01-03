
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from typing import List

class NotificationService:
    def __init__(self, smtp_settings: dict):
        self.smtp_settings = smtp_settings

    async def send_appointment_reminder(self, task: 'Task') -> bool:
        """Send reminder for upcoming appointment."""
        if not task.client:
            return False

        template = self._get_reminder_template(task)
        return await self._send_email(
            to_email=task.client,
            subject="Appointment Reminder",
            body=template
        )

    async def notify_waitlist(self, task: 'Task') -> List[bool]:
        """Notify waitlisted clients about availability."""
        results = []
        for client in task.waitlist:
            success = await self._send_email(
                to_email=client,
                subject="Appointment Slot Available",
                body=self._get_waitlist_template(task)
            )
            results.append(success)
        return results