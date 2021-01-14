from django.urls import path

from . import views

from .feeds import LatestPostsFeed


app_name = 'myblog'

urlpatterns = [
    path('', views.PostList, name='post_list'),
    # additional URL to list posts by tag
    path('tag/<slug:tag_slug>/', views.PostList, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.SinglePost, name='single_post'),
    path('<int:post_id>/share', views.PostShare, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
    ]
