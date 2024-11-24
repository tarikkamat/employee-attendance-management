from rest_framework_simplejwt.views import TokenObtainPairView

from attendancelog.models import AttendanceLog
from project.core.responses import APIResponse
from project.core.types import AttendancesTypes
from project.core.views import BaseListView, BaseDetailView
from users.api.serializers import UserSerializer, MyTokenObtainPairSerializer
from users.models import User


class GetAllUsers(BaseListView):
    serializer_class = UserSerializer
    model = User

    def post(self, request):
        # Override edilen post methodu silinirse BaseModel ile bu özellik aktif edilebilir.
        return APIResponse.bad_request({"message:": "This feature is disabled.", "status": False})


class GetUser(BaseDetailView):
    serializer_class = UserSerializer
    model = User

    def delete(self, request, pk):
        # Override edilen delete methodu silinirse BaseModel ile bu özellik aktif edilebilir.
        return APIResponse.bad_request({"message:": "This feature is disabled.", "status": False})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            try:
                user = User.objects.get(email=request.data['email'])
                AttendanceLog.objects.create(user=user, action=AttendancesTypes.LOGIN)
            except User.DoesNotExist:
                pass
        return response


class MyTokenValidateView(BaseDetailView):
    def get(self, request):
        return APIResponse.success({"message": "Token is valid.", "status": True})


class MyTokenRemoveView(BaseDetailView):
    def get(self, request):
        if request.user.is_authenticated:
            AttendanceLog.objects.create(user=request.user, action=AttendancesTypes.LOGOUT)
        return APIResponse.success({"message": "Token is removed.", "status": True})
