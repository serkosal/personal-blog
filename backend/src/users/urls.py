from django.urls import path, include

from .views import (
    profile,
    detail,
    RegisterView,
    ProfileUpdate,
    toggle_follow,
)

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('profile/<int:user_id>/', detail, name='detail'),
    path('profile/<int:user_id>/e/', ProfileUpdate.as_view(), name='edit'),
    path('profile/<int:user_id>/follow/', toggle_follow, name='toggle_follow'),
]
