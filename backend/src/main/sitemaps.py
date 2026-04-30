from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from blog.models import Post

class StaticSitemap(Sitemap):
    i18n = True
    alternates = True
    # x_default = True
    
    def items(self):
        return ['index', 'blog:index']
    
    def location(self, obj: str):
        return reverse(obj)


class PostSitemap(Sitemap):
    
    i18n = True
    alternates = True
    # x_default = True
    
    def items(self):
        return Post.posts.filter(published_at__lte=timezone.now())

    
    def lastmod(self, obj: Post):
        return obj.published_at

