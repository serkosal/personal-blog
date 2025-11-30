from django.urls import path

from .views import index, detail, edit, api_root

app_name = "blog"
urlpatterns = [
    path('',                 index,  name="index"),
    path('<int:post_id>/',   detail, name="detail"),
    path('<int:post_id>/e/', edit,   name="edit"),
    
    path('api/', api_root, name="api-root"), # GET, POST, 
    # path('api/<int:post_id>/', api_root, name="api-root"), # GET POST DELETE PATCH
] 