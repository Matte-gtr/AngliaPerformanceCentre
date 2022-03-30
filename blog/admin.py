from django.contrib import admin
from .models import BlogCategory, BlogPost, BlogPostVideo,\
    BlogPostComment


admin.site.register(BlogCategory)
admin.site.register(BlogPost)
admin.site.register(BlogPostVideo)
admin.site.register(BlogPostComment)
