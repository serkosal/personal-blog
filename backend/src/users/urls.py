from django.urls import path, include

from .views import profile, detail, api_detail, RegisterView, ProfileUpdate

app_name = "users"
urlpatterns = [
    
    path('', include("django.contrib.auth.urls")),
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', profile, name='profile'),
    path('profile/<int:user_id>/', detail, name="detail"),
    path('profile/<int:user_id>/e/', ProfileUpdate.as_view(), name="edit"),
    
    path('api/profile/<int:user_id>/', api_detail, name='api-detail'),
]