from rest_framework_simplejwt.views import TokenObtainPairView

from project.core.views import BaseListView, BaseDetailView
from users.api.serializers import UserSerializer, MyTokenObtainPairSerializer
from users.models import User


class GetAllUsers(BaseListView):
    serializer_class = UserSerializer
    model = User


class GetUser(BaseDetailView):
    serializer_class = UserSerializer
    model = User


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
