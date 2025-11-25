from django.urls import path

from .views import index, detail, edit

app_name = "blog"
urlpatterns = [
    path('',                 index,  name="index"),
    path('<int:post_id>/',   detail, name="detail"),
    path('<int:post_id>/e/', edit,   name="edit"), 
] 