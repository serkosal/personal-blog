"""File with views for 'blog' Django app."""

from django.contrib.auth.models import AbstractUser
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from allauth.account.decorators import verified_email_required
from markdown_it import MarkdownIt
from markdown_it.presets import gfm_like
from markdown_it.common.utils import escapeHtml
from markdown_it.renderer import RendererHTML

from .forms.forms import PostCreateForm, PostEditForm
from .models import Post
# from .serializers.post import PostSerializer
# from .serializers.post_content import PostContentSchema

class MyRenderer(RendererHTML):
    
    def fence(self, tokens, idx, options, env):
        token = tokens[idx] 
        
        return  (
            '<pre>' + 
              '<code class="GFM-editor-code-block"' + self.renderAttrs(token) + ">" + 

                escapeHtml(token.content) + 
            "</code></pre>\n"
        )
    
    def code_block(self, tokens, idx, options, env):

        token = tokens[idx] 
        return  (
            '<pre class="GFM-editor">' '<codes class="GFM-editor-code-block"'
            + self.renderAttrs(token)
            + ">" + escapeHtml(token.content)
            + "</code></pre>\n"
        )
    
md_preset = gfm_like.make()
md_preset['options']['breaks'] = True
md = (
    MarkdownIt('gfm-like', md_preset['options'], renderer_cls=MyRenderer)
    .enable('table')
)

class PostList(ListView):
    """Render a page with the list of posts."""
    
    model = Post
    context_object_name = 'posts_list'
    paginate_by = 10
    page_kwarg = 'page'

    def get_queryset(self):
        """Get the list of posts.
        
        Args:
            self (PostList): instance of the PostList class.
        
        """
        user = self.request.user
        self.posts = Post.posts.visible_to(user)
        
        tags = self.request.GET.get("tags", '')
        if tags:
            tags_list = [t.lower() for t in tags.split(',')]
            self.posts = self.posts.filter(tags__name__in=tags_list)

        
        self.posts = self.posts.order_by(
            '-published_at', '-last_edited'
        )

        return self.posts

    def get_context_data(self, **kwargs):
        """Get the context data.
        
        Args:
            self (PostList): instance of the PostList class.
            kwargs: Arbitrary keyword arguments.
        
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Latest posts'
        paginator, page_obj, self.posts, self.is_paginated = self.paginate_queryset(
            self.posts, self.paginate_by
        )
        context['page_obj'] = page_obj
        
        context['pages_links'] = [i for i in range( max(2, page_obj.number - 5), min(page_obj.paginator.num_pages, page_obj.number + 5) ) ]
        
        parsed_posts: list[tuple[str, Post]] = []
        for post in self.posts:
            parsed_posts.append((md.render(post.content), post))
        context['parsed_posts'] = parsed_posts

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
    
    def get_object(self):
        post: Post = super().get_object()
        
        # other staff members couldn't increase view count 
        if (self.request.user != post.author and not self.request.user.is_staff 
            and post.is_published()
        ):
            post.views_num += 1
            post.save(force_update=True)
        
        return post
        

    def get_context_data(self, **kwargs):
        """Get the context data.
        
        Args:
            self (PostDetail): instance of the PostDetail class.
            kwargs: Arbitrary keyword arguments.

        """
        
        context = super().get_context_data(**kwargs)
        post: Post = context['post']
        
        user = self.request.user

        context['can_edit'] = post.can_edit(user)
        context['tags'] = post.tags.all()
        
        context['post_content'] = md.render(post.content)

        return context


@method_decorator(verified_email_required, name='dispatch')
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


@method_decorator(verified_email_required, name='dispatch')
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
@method_decorator(verified_email_required, name='dispatch')
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

    def form_valid(self, form: PostEditForm):
        """Execute after successfully validate form.

        Args:
            self (PostUpdate): instance of the PostUpdate class.
            form (BaseModelForm): instance of a validated form.

        """
        response = super().form_valid(form) 
        post = form.instance
        if not post.can_edit(self.request.user):
            form.add_error(None, "You don't have permission to edit this post.")
            return self.form_invalid(form)
        
        # saving tags
        tags = form.cleaned_data.get('tags')
        if tags is not None:
            self.object.tags.set(tags)
        
        return response
    
    def form_invalid(self, form):
        """Sends A JSON Payload with form errors."""
        
        return JsonResponse({
            "success": "false", "errors": form.errors, 
            "non_field_errors": form.non_field_errors()
        })

    def get_success_url(self):
        """Get the link to a newly created post.
        
        Args:
            self (PostUpdate): instance of the PostUpdate class.

        """
        post: Post = self.object
        return reverse('blog:detail', kwargs={'pk': post.pk})


# def api_root(req: HttpRequest) -> JsonResponse:
#     """Get the posts list in JSON format.

#     Args:
#         req (HttpRequest): HTTP request from the client.

#     Returns:
#         JsonResponse: JSON response to the client.

#     """
#     if req.method == 'GET':
#         user = req.user

#         posts = Post.posts.visible_to(user)

#         for post in posts:
#             PostContentSchema.model_validate(post.content)

#         serializer = PostSerializer(posts, many=True, context={'request': req})

#         return JsonResponse({'posts': serializer.data})

#     # add csrf token check
#     elif req.method == 'POST':
#         if not req.user.is_authenticated:
#             return JsonResponse(
#                 {'error': 'you should be authorized before create any posts!'},
#                 status=401,
#             )

#         data = JSONParser().parse(req)

#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         else:
#             return JsonResponse(serializer.errors, status=400)

#     else:
#         return JsonResponse(
#             {'error': f'{req.method} is not allowed!'}, status=405
#         )


# def api_detail(req: HttpRequest, post_id: int) -> JsonResponse:  # noqa: PLR0911
#     """Get the posts list in JSON format.

#     Args:
#         req (HttpRequest): HTTP request from the client.
#         post_id (int): Post's id.

#     Returns:
#         JsonResponse: JSON response to the client.
    
#     """
#     post: Post
#     try:
#         post = Post.objects.get(pk=post_id)
#     except Post.DoesNotExist:
#         return JsonResponse(
#             {'error': f'Requested post with id={post_id} does not exist!'},
#             status=404,
#         )

#     if req.method == 'GET':
#         if not post.can_see(req.user):
#             return JsonResponse(
#                 {'error': 'You do not have permissions to see this post!'},
#                 status=403,
#             )

#         serializer = PostSerializer(post, context={'request': req})
#         return JsonResponse(serializer.data)

#     if not req.user.is_authenticated:
#         return JsonResponse(
#             {'error': 'You should be authorized before edit any posts!'},
#             status=401,
#         )

#     if not post.can_edit(req.user):
#         return JsonResponse(
#             {'error': 'You do not have permissions to edit this post!'},
#             status=403,
#         )

#     if req.method == 'DELETE':
#         res = post.delete()
#         return JsonResponse({'deleted': res[0]}, status=200)

#     elif req.method == 'PATCH':
#         data = JSONParser().parse(req)

#         serializer = PostSerializer(post, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.errors, status=400)

#     else:
#         return JsonResponse(
#             {'error': f'{req.method} is not allowed!'}, status=405
#         )
