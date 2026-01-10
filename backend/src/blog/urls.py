"""file with URL patterns for 'blog' Django app."""

from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('c/', views.PostCreate.as_view(), name='create'),
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('<int:pk>/del/', views.PostDelete.as_view(), name='delete'),
    path('<int:pk>/e/', views.PostUpdate.as_view(), name='edit'),
    # GET, POST
    path('api/posts/', views.api_root, name='api-root'),
    # GET POST DELETE PATCH
    path('api/posts/<int:post_id>/', views.api_detail, name='api-detail'),
]
