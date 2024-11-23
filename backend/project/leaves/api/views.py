from rest_framework_simplejwt.views import TokenObtainPairView

from project.core.responses import APIResponse
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
