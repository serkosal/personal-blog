from django.urls import path, include

from .views import profile, api_detail, RegisterView

app_name = "users"
urlpatterns = [
    
    path('', include("django.contrib.auth.urls")),
    path('profile/', profile, name='profile'),
    path('register/', RegisterView.as_view(), name="register"),
    
    path('api/profile/<int:profile_id>/', api_detail, name='api-detail'),
]