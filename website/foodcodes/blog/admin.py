from django.contrib import admin
from .models import Post, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['author']
    list_display = ['author', 'title']


class CommentAdmin(admin.ModelAdmin):
    list_filter = ['author', 'post']
    list_display = ['author', 'post', 'comment']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
