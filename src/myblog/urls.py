from django.urls import path

from . import views


app_name = 'myblog'

urlpatterns = [
    # path('', views.PostList, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.SinglePost, name='single_post'),
    path('<int:post_id>/share', views.PostShare, name='post_share'),
    ]
