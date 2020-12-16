from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from myblog.models import Post


class PostListView(ListView):

    # build a generic QuerySet
    queryset = Post.published.all()
    # use conrext variable 'posts' for a query results
    context_object_name = 'posts'
    # 3 posts in each page
    paginate_by = 3
    # use a custom template name
    template_name = 'blog/post/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['GET_PARAMS'] = '&'.join(
            f'{key}={value}'
            for key, value in self.request.GET.items()
            if key != 'page'
        )
        context['object_count'] = context['object_list'].count()
        return context


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
