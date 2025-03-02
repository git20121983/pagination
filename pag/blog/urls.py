
from blog.views import  blog_list_view, post_detail, post_comment
from django.urls import path, include


app_name = 'blog'

urlpatterns = [
    path('blog/', include([
        path('', blog_list_view, name='blog-list'),
        
        path('tag/<slug:tag_slug>/', blog_list_view, name='post-list-by-tag'),
        path('<slug:post_slug>/', post_detail, name='post-detail'),
        path('<int:post_id>/comment/', post_comment, name = 'post-comment'),
    ])),
]
