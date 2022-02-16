from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogPostImage, BlogPostVideo


admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(BlogPostImage)
admin.site.register(BlogPostVideo)
