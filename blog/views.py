from django.shortcuts import render
from .models import BlogPost


def blog(request):
    """ a view to display the blog page """
    blog_posts = BlogPost.objects.all().order_by('added_on')
    template = "blog/blog.html"
    context = {
        'title': 'blog',
        'section': 'blog',
        'blog_posts': blog_posts,
    }
    return render(request, template, context)
