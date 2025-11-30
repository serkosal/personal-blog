from django.urls import path

from .views import index, detail, edit, api_root, api_detail

app_name = "blog"
urlpatterns = [
    path('',                 index,  name="index"),
    path('<int:post_id>/',   detail, name="detail"),
    path('<int:post_id>/e/', edit,   name="edit"),
    
    path('api/posts/', api_root, name="api-root"), # GET, POST
    
    # GET POST DELETE PATCH
    path('api/posts/<int:post_id>/', api_detail, name="api-detail"), 
]
