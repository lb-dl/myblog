from django.shortcuts import get_object_or_404, render
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from myblog.models import Post

from .forms import EmailPostForm

from django.core.mail import send_mail


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


def PostShare(request, post_id):

    # retrieve the post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    # check if the form is submitted
    if request.method == 'POST':
        # create a form instance using data from the request.POST
        form = EmailPostForm(request.POST)
        # validate form's fields
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cleaned_data['name']} recommends you to read" \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n]" \
                      f"{cleaned_data['name']}\'s comments: {cleaned_data['comments']}"
            send_mail(subject, message, 'lbdltest77@gmail.com', [cleaned_data['to']])
            sent = True
    else:
        # having a Get request create a new form instance to display an empty form in the template
        form = EmailPostForm
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
