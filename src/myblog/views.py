from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from myblog.models import Post


def PostList(request):
    # posts = Post.published.all()

    object_list = Post.published.all()

    # instantinate a paginator class with a number of objects to be displayed
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page') # get the current page
    try:
        posts = paginator.page(page) # obtain the objects of a desired page
    except PageNotAnInteger: # if the page isn't an integer deliver the first one
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'page': page, # pass page number and retrieved objects to the template
        'posts': posts},
    )


def SinglePost(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, 'blog/post/single.html', {'post': post})
