"""File with views for 'blog' Django app."""

from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from rest_framework.parsers import JSONParser

from .forms.forms import PostCreateForm, PostEditForm
from .models import Post
from .serializers.post import PostSerializer
from .serializers.post_content import PostContentSchema


class PostList(ListView):
    """Render a page with the list of posts."""
    
    model = Post
    context_object_name = 'posts_list'

    def get_queryset(self):
        """Get the list of posts.
        
        Args:
            self (PostList): instance of the PostList class.
        
        """
        user = self.request.user

        posts = Post.posts.visible_to(user).order_by('-published_at')

        return posts

    def get_context_data(self, **kwargs):
        """Get the context data.
        
        Args:
            self (PostList): instance of the PostList class.
            kwargs: Arbitrary keyword arguments.
        
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Latest posts'

        return context


class PostDetail(DetailView):
    """Render the required post."""
    
    model = Post
    context_object_name = 'post'

    def get_queryset(self):
        """Get the required post.
        
        Args:
            self (PostDetail): instance of the PostDetail class.
        
        """
        user = self.request.user

        self.posts = Post.posts.visible_to(user)

        return self.posts

    def get_context_data(self, **kwargs):
        """Get the context data.
        
        Args:
            self (PostDetail): instance of the PostDetail class.
            kwargs: Arbitrary keyword arguments.

        """
        post: Post = self.get_object()
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['can_edit'] = post.can_edit(user)

        return context


class PostDelete(DeleteView):
    """Deletes the required post."""
    
    model = Post
    success_url = reverse_lazy('blog:index')
    context_object_name = 'post'

    def get_queryset(self):
        """Get the required post.
        
        Args:
            self (PostDelete): instance of the PostDelete class.
        
        """
        user = self.request.user

        return Post.posts.editable_to(user)


class PostCreate(CreateView):
    """Creates a new post."""
    
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm
    
    object: Post | None

    def form_valid(self, form):
        """Create a new post.
        
        Args:
            self (PostCreate): instance of the PostCreate class.
            form (BaseModelForm): instance of a validated form.
        
        """
        post: Post = form.instance
        user: AbstractUser = self.request.user

        if user.is_anonymous or not user.is_active:
            return False

        post.author = user
        return super().form_valid(form)


    def get_success_url(self):
        """Get the link to a newly created post.
        
        Args:
            self (PostCreate): instance of the PostCreate class.
        
        """
        return reverse('blog:edit', kwargs={'pk': self.object.pk})


# renders title, is_published fields through standart django forms
# renders content field through editor.js plugin
class PostUpdate(UpdateView):
    """Updates the required post."""
    
    model = Post
    template_name = 'blog/post_update.html'
    form_class = PostEditForm

    def get_queryset(self):
        """Get the required post.
        
        Args:
            self (PostUpdate): instance of the PostUpdate class.
        
        """
        user = self.request.user

        self.posts = Post.posts.editable_to(user)

        return self.posts

    def form_valid(self, form):
        """Execute after successfully validate form.

        Args:
            self (PostUpdate): instance of the PostUpdate class.
            form (BaseModelForm): instance of a validated form.

        """
        post: Post = form.instance
        user: AbstractUser = self.request.user

        if not post.can_edit(user):
            form.add_error(None, "You don't have permission to edit this post.")
            return self.form_invalid(form)
        
        return super().form_valid(form)

    def get_success_url(self):
        """Get the link to a newly created post.
        
        Args:
            self (PostUpdate): instance of the PostUpdate class.

        """
        post: Post = self.object
        return reverse('blog:detail', kwargs={'pk': post.pk})


def api_root(req: HttpRequest) -> JsonResponse:
    """Get the posts list in JSON format.

    Args:
        req (HttpRequest): HTTP request from the client.

    Returns:
        JsonResponse: JSON response to the client.

    """
    if req.method == 'GET':
        user = req.user

        posts = Post.posts.visible_to(user)

        for post in posts:
            PostContentSchema.model_validate(post.content)

        serializer = PostSerializer(posts, many=True, context={'request': req})

        return JsonResponse({'posts': serializer.data})

    # add csrf token check
    elif req.method == 'POST':
        if not req.user.is_authenticated:
            return JsonResponse(
                {'error': 'you should be authorized before create any posts!'},
                status=401,
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
            {'error': f'{req.method} is not allowed!'}, status=405
        )


def api_detail(req: HttpRequest, post_id: int) -> JsonResponse:  # noqa: PLR0911
    """Get the posts list in JSON format.

    Args:
        req (HttpRequest): HTTP request from the client.
        post_id (int): Post's id.

    Returns:
        JsonResponse: JSON response to the client.
    
    """
    post: Post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse(
            {'error': f'Requested post with id={post_id} does not exist!'},
            status=404,
        )

    if req.method == 'GET':
        if not post.can_see(req.user):
            return JsonResponse(
                {'error': 'You do not have permissions to see this post!'},
                status=403,
            )

        serializer = PostSerializer(post, context={'request': req})
        return JsonResponse(serializer.data)

    if not req.user.is_authenticated:
        return JsonResponse(
            {'error': 'You should be authorized before edit any posts!'},
            status=401,
        )

    if not post.can_edit(req.user):
        return JsonResponse(
            {'error': 'You do not have permissions to edit this post!'},
            status=403,
        )

    if req.method == 'DELETE':
        res = post.delete()
        return JsonResponse({'deleted': res[0]}, status=200)

    elif req.method == 'PATCH':
        data = JSONParser().parse(req)

        serializer = PostSerializer(post, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    else:
        return JsonResponse(
            {'error': f'{req.method} is not allowed!'}, status=405
        )
