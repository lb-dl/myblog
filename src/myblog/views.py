from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector

from myblog.models import Post

from .forms import CommentForm, EmailPostForm, SearchForm

from django.core.mail import send_mail
from django.db.models import Count

from taggit.models import Tag


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
    ''' get all active comments for this post using the manager 'comments'
     that was created with a related_name in the Comment model '''
    comments = post.comments.filter(active=True)

    # initialize a variable to save a new comment later
    new_comment = None
    # check if a new comment was added
    if request.method == 'POST':
        # instantiate the form using the submitted data and validate it
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid:
            # create Comment object but don't save it to DB
            new_comment = comment_form.save(commit=False)
            # assign the current post to this comment
            new_comment.post = post
            new_comment.save()
    # build a form instance if the view is called by a GET request
    else:
        comment_form = CommentForm()
    # retrieve a list of ids for all tags of the current post. value_list returns a tuple of ids
    post_tags_ids = post.tags.values_list('id', flat=True)
    # get all posts that contain any of these tags, excluding the current post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # use Count() to generate the number of tags shared with all the tags queried
    # to display resent posts first for the post with the same number of shared tags
    # retrieve only the first four posts
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                        .order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/single.html',
        {'post': post,
         'comments': comments,
         'new_comment': new_comment,
         'comment_form': comment_form,
         'similar_posts': similar_posts
         })


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
            subject = f"{cleaned_data['name']} recommends you to read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cleaned_data['name']}\'s comments: {cleaned_data['comments']}"
            send_mail(subject, message, 'djangoproject20@gmail.com', [cleaned_data['to']])
            sent = True
    else:
        # having a Get request create a new form instance to display an empty form in the template
        form = EmailPostForm
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def PostList(request, tag_slug=None):
    # the optional parameter 'tag_slug' will be passed in the URL

    object_list = Post.published.all()
    tag = None

    # check if there's a given tag_slug
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # filter the list of the posts by the ones that contain the given tag
        object_list = object_list.filter(tags__in=[tag])

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
        'posts': posts,
        'tag': tag},
    )

def post_search(request):
    # instantiate the SearchForm form
    form = SearchForm()
    query = None
    results = []
    # check if the form is submitted, looking for a query param in the request.Get dict
    # using the GET method, so that the resulting URL includes the query param
    if 'query' in request.GET:
        # instantiate the submitted form with the submitted GET data
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # search for posts with a custom SearchVector instance built with title and body fields
            results = Post.published.annotate(
                search=SearchVector('title', 'body'),).filter(search=query)
    return render(request, 'blog/post/search.html',
                  {'form': form, 'query': query, 'results': results})
