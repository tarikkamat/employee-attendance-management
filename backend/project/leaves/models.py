from django.db import models

from project.db.models import BaseModel
from users.models import User


class Leave(BaseModel):
    fk_user_id = models.ForeignKey(User, db_column="fk_user_id", on_delete=models.CASCADE, related_name="leaves")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_leaves")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default="pending")
    reason = models.TextField(null=True, blank=True)
