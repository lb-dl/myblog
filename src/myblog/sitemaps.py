from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    # get the objects that items() returns and return the last time the object was modified
    def lastmod(self, obj):
        return obj.updated
