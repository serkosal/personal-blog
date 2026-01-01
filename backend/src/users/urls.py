from django.urls import path, include

from .views import profile, detail, api_detail, RegisterView

app_name = "users"
urlpatterns = [
    
    path('', include("django.contrib.auth.urls")),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', profile, name='profile'),
    path('profile/<int:profile_id>/', detail, name="detail"),
    
    path('api/profile/<int:profile_id>/', api_detail, name='api-detail'),
]