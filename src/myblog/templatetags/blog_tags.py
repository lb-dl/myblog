from django import template

from ..models import Post

from django.db.models import Count



# use a variable 'register' to register our own template tag
register = template.Library()

# create a simple template tag that returns the number of posts published so far
# the decorator is used to register a function as a simple tag
# Django will use the function's name as a tag name
@register.simple_tag
def total_posts():
    return Post.published.count()

# register the template tag and specify the template that will be rendered with the returned values
@register.inclusion_tag('blog/post/latest_posts.html')
# use the optional parameter 'count' to specify the number of posts that will be shown
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    # use annotate function to aggregate the total number of comments for each post
    return Post.published.annotate(total_comments=Count('comments'))\
                        .order_by('-total_comments')[:count]