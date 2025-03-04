from django import template
from ..models import Blog
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.simple_tag
def total_posts():
    return Blog.objects.count()

@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Blog.objects.order_by('-date_posted')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=4):
    return Blog.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format (text):
    return mark_safe(markdown.markdown(text))