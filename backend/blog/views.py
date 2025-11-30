from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from .models import Post

def index(req: HttpRequest) -> HttpResponse:
    
    latest_posts = Post.objects.order_by("-published_at")
    
    # dynamically add filter
    if not req.user.has_perm("blog.see_others_unpublished"):
        latest_posts = latest_posts.filter(is_published=True) 
    
    context = {
        "latest_posts": latest_posts[:5],
        "title": "Latest posts"
    }
    
    return render(req, "blog/index.html", context=context)


def detail(req: HttpRequest, post_id: int) -> HttpResponse:
    
    post = get_object_or_404(Post, pk=post_id)
    
    if not post.can_see(req.user):
        raise PermissionDenied("You don't have permissions to see this Post.")
    
    context = {
        "post": post,
        "title": post.title
    }
    
    return render(req, "blog/detail.html", context=context)


def edit(req: HttpRequest, post_id: int) -> HttpRequest:
    post = get_object_or_404(Post, pk=post_id)
    
    if not post.can_edit(req.user):
        raise PermissionDenied("You don't have permissions to edit this Post.")
    
    context = {
        "post": post,
        "title": f"editing {post.title}"
    }
    
    return render(req, "blog/edit.html", context=context)