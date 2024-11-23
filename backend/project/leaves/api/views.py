from leaves.api.serializers import LeaveSerializer
from leaves.models import Leave
from project.core.views import BaseListView, BaseDetailView


class GetAllLeaves(BaseListView):
    serializer_class = LeaveSerializer
    model = Leave


class GetLeave(BaseDetailView):
    serializer_class = LeaveSerializer
    model = Leave
