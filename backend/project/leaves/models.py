from django.db import models

from project.core.types import LeaveStatusTypes, LeaveReasonTypes
from project.db.managers import BaseManager
from project.db.models import BaseModel
from users.models import User


class Leave(BaseModel):
    fk_user_id = models.ForeignKey(User, db_column="fk_user_id", on_delete=models.CASCADE, related_name="leaves")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=LeaveStatusTypes.choices)
    reason = models.CharField(max_length=50, choices=LeaveReasonTypes.choices)

    objects = BaseManager()
