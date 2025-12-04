from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path('',          views.PostList.as_view(),  name="index"),
    path('<int:pk>/', views.PostDetail.as_view(), name="detail"),
    path('<int:pk>/del/', views.PostDelete.as_view(), name="delete"),
    path('<int:pk>/e/', views.edit,   name="edit"),
    
    path('api/posts/', views.api_root, name="api-root"), # GET, POST
    
    # GET POST DELETE PATCH
    path('api/posts/<int:post_id>/', views.api_detail, name="api-detail"), 
]
