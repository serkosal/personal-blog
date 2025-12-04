from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView, DetailView, DeleteView, UpdateView, CreateView
)
from rest_framework.parsers import JSONParser

from .models import Post
from .serializers import PostSerializer

class PostList(ListView):
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts_list"

    def get_queryset(self):
        user = self.request.user
        
        posts = Post.posts.visible_to(user).order_by("-published_at")

        return posts
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Latest posts"
        
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"    
    
    def get_queryset(self):
        user = self.request.user
        
        self.posts = Post.posts.visible_to(user)
        
        return self.posts
    
    
    def get_context_data(self, **kwargs):
        post: Post = self.get_object()
        user = self.request.user
        
        context = super().get_context_data(**kwargs)
        context["can_edit"] = post.can_edit(user)
        
        return context


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:index")
    template_name = "blog/confirm_delete.html"
    context_object_name = "post"
    
    def get_queryset(self):
        user = self.request.user
        
        return Post.posts.visible_to(user)


# renders title, is_published fields through standart django forms
# renders content field through editor.js plugin
def edit(req: HttpRequest, pk: int) -> HttpRequest:
    post = get_object_or_404(Post, pk=pk)
    
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
        serializer = PostSerializer(posts, many=True, context={'request': req})
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
        
        serializer = PostSerializer(post, context={'request': req})
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

