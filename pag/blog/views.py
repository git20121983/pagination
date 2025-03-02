from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .models import Blog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm, EmailPostForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.db.models import Count

from taggit.models import Tag

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Blog,
        id = post_id,
    )
    
    comment = None
    #Коментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Саздать обект класса Comment не сохраняя его в базе
        comment = form.save(commit=False)
        # назначить пост комментарию 
        comment.post = post
        # сохранить коментарий в базе данных
        comment.save()
    return render(request, 'blog/comment.html', {
        'post':post,
        'form':form,
        'comment':comment
    })
    
 
def blog_list_view(request, tag_slug=None):
    # Получаем все объекты Blog
    blog_list = Blog.objects.all()
    tag = None
    
     # Фильтрация по тегу, если передан tag_slug            
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        blog_list = blog_list.filter(tags__in=[tag])
    
    # Пагинация для основного списка блогов
    paginator = Paginator(blog_list, 2)
    page = request.GET.get('page')
    
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
    
    # Пагинация для дополнительного списка блогов
    other_blog_posts = Blog.objects.all()
    
    paginator_other = Paginator(other_blog_posts, 2)
    page_two = request.GET.get('other-page')
    
    try:
        other_blog_posts = paginator_other.page(page_two)
    except PageNotAnInteger:
        other_blog_posts = paginator_other.page(1)
    except EmptyPage:
        other_blog_posts = paginator_other.page(paginator_other.num_pages)
    
    # Создаем контекст для передачи в шаблон
    context = {
        'object_list': object_list,
        'other_blog_posts': other_blog_posts,
        'tag':tag,
    }
    
    return render(request, 'blog/blog_list.html',  context)



    
def post_detail(request, post_slug):
    post = get_object_or_404(
        Blog,
        slug = post_slug
        )
    
#Список активных коментариев к этому посту
    comments = post.comments.filter(active=True)
# форма для коментирования пользователями
    form =CommentForm()
    
# Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts =  Blog.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_posted')[:4]
        
    return render(request, 'blog/blog_detail.html', {'post': post, 'comments': comments, 'form':form, 'similar_posts':similar_posts})
 
    


    
# This is the view that will handle the email sharing of blog posts
    
def email_share (request, blog_id):
    post = get_object_or_404(
        Blog,
        id=blog_id,
        
    )
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_url( 
                post.get_absolute_url()
                )
            
            subject = ( 
                f"{cd['name']} рекомендуем тебе читать " 
                f"{post.title}"
                )
            message = (
                f"Прочитай { post.title } на { post_url }\n\n"
                f"{cd['name']}\'s коментарий: {cd['comments']}"
                )
            
            send_mail(
                subject,
                message,
                'ted20121983@gmail.com',
                [cd['email_to']]
            )
            
    else:
        form = EmailPostForm()
        
        return render(request, 'blog/share.html', {'sent': sent, 'post': post, 'form': form})