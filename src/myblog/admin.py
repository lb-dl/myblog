from myblog.models import Comment, Post

from django.contrib import admin

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', ]
    list_filter = ['status', 'created', 'publish','author', ]
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active', ]
    list_filter = ['active', 'created', 'updated', ]
    search_fields = ('name', 'email', 'body')


admin.site.unregister(Post)
admin.site.register(Post, PostAdmin)
