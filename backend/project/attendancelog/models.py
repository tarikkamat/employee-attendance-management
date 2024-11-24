from django.db import models

from project.core.types import AttendancesTypes
from project.db.models import BaseModel
from users.models import User


class AttendanceLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_logs')
    timestamp = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=10, choices=AttendancesTypes.choices)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"
