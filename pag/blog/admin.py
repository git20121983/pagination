from django.contrib import admin
from .models import Blog, Comment
# Register your models here.
@admin.register(Blog)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'date_posted', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['date_posted']
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body', 'email']
    