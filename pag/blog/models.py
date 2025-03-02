from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    
    
    def __str__(self):
        return self.title
    
   
    
  

    def get_absolute_url(self):
        return reverse('post:post-detail', args=[self.slug]) #kwargs={'slugs': self.slug}
            
class Comment(models.Model):
    post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField( auto_now_add=True )
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        
    def __str__(self):
        return f'Comment by { self.name } on {self.post}'