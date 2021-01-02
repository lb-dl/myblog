import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from django.contrib.sitemaps.views import sitemap
from myblog.sitemaps import PostSitemap

sitemaps = {'posts': PostSitemap, }

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('myblog/', include('myblog.urls', namespace='myblog')),
    path(
        'sitemap.xml',
        sitemap, {'sitemaps': sitemaps},
        name= 'django.contrib.sitemaps.views.sitemap'
    )
]
