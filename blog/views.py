from django.shortcuts import render
from .models import BlogPost, BlogCategory


def blog(request):
    """ a view to display the blog page """
    blog_posts = BlogPost.objects.all().order_by('added_on')
    for post in blog_posts:
        post.short_body = post.post_body[:200]
    categories = BlogCategory.objects.all()
    template = "blog/blog.html"
    context = {
        'title': 'blog',
        'section': 'blog',
        'blog_posts': blog_posts,
        'categories': categories,
    }
    return render(request, template, context)
