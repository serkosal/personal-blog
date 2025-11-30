from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Post
from .serializers import PostSerializer

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
        "title": post.title,
        "can_edit": post.can_edit(req.user)
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


def api_root(req: HttpRequest) -> JsonResponse:
    
    if req.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse({"posts": serializer.data})
    
    # add csrf token check
    elif req.method == "POST":
        
        if not req.user.is_authenticated:
            return JsonResponse(
                {"error": "you should be authorized before create any posts!"},
                status=401
            )
        
        data = JSONParser().parse(req)
        
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)
        
    else:
        return JsonResponse(
                {"error": f"{req.method} is not allowed!"},
                status=405
            )


def api_detail(req: HttpRequest, post_id: int) -> JsonResponse:
    
    post: Post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse(
            {"error": f"Requested post with id={post_id} does not exist!"},
            status=404
        )

    if req.method == "GET":
        
        if not post.can_see(req.user):
            return JsonResponse(
            {"error": "You do not have permissions to see this post!"},
            status=403
        )
        
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    
    if not req.user.is_authenticated:
        return JsonResponse(
            {"error": "You should be authorized before edit any posts!"},
            status=401
        )
        
    if not post.can_edit(req.user):
        return JsonResponse(
            {"error": "You do not have permissions to edit this post!"},
            status=403
        )
    
    if req.method == "DELETE":
        res = post.delete()
        return JsonResponse({"deleted": res[0]}, status=200)
    
    elif req.method == "PATCH":
        data = JSONParser().parse(req)
        
        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    else:
        return JsonResponse(
                {"error": f"{req.method} is not allowed!"},
                status=405
            )

