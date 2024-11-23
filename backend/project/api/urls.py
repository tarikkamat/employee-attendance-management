from django.urls import path

from project.helpers import get_api_slug
from users.api import views as user_views
from users.models import User
from leaves.models import Leave
from leaves.api import views as leave_views

urlpatterns = [
    path(get_api_slug(User) + "/", user_views.GetAllUsers.as_view()),
    path(get_api_slug(User) + "/<int:pk>", user_views.GetUser.as_view()),
    path(get_api_slug(Leave) + "/", leave_views.GetAllLeaves.as_view()),
    path(get_api_slug(Leave) + "/<int:pk>", leave_views.GetLeave.as_view()),
    path('auth/login', user_views.MyTokenObtainPairView.as_view())
]
