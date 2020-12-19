from django.db import models

from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

# create a custom manager to retrieve all posts with the published status

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):

    # the default manger
    objects = models.Manager()
    # custom manager
    published = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)

    # a field that will be used in urls
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # OneToMany relationship (each post is written by user and every user can write many posts)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')

    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updates = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # sort 'published' in descending order, so post published recently will appear first
        ordering = ('-publish',)

    # make 'title' human-readable representation
    def __str__(self):
        return self.title

    # build the canonical URLs for Post objects
    def get_absolute_url(self):
        return reverse('myblog:single_post',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug]
                       )

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
