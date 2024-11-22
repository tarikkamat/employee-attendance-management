from django.urls import path

from project.helpers import get_api_slug
from users.api import views as user_views
from users.models import User

urlpatterns = [
    path(get_api_slug(User) + "/", user_views.GetAllUsers.as_view()),
    path(get_api_slug(User) + "/<int:pk>", user_views.GetUser.as_view()),
    path('auth/login', user_views.MyTokenObtainPairView.as_view())
]
