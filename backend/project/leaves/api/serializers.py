from rest_framework import serializers

from leaves.models import Leave


class LeaveSerializer(serializers.ModelSerializer):
    model = Leave
    fields = '__all__'
