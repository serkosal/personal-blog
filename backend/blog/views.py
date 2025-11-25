#from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Post

# Create your views here.

def index(req: HttpRequest) -> HttpResponse:
    
    latest_posts = Post.objects.order_by("-published_at")[:5]
    
    context = {
        "latest_posts": latest_posts,
        "title": "Latest posts"
    }
    
    return render(req, "blog/index.html", context=context)


def detail(req: HttpRequest, post_id: int) -> HttpResponse:
    
    post = get_object_or_404(Post, pk=post_id)
    
    context = {
        "post": post,
        "title": post.title
    }
    
    return render(req, "blog/detail.html", context=context)


def edit(req: HttpRequest, post_id: int) -> HttpRequest:
    post = get_object_or_404(Post, pk=post_id)
    
    context = {
        "post": post,
        "title": f"editing {post.title}"
    }
    
    return render(req, "blog/edit.html", context=context)