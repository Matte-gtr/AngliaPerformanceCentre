from django.shortcuts import render, get_object_or_404
from .models import BlogPost, BlogCategory
from user_management.views import paginator_helper


def blog(request):
    """ a view to display the blog page """
    category = "All"
    filter_cat = None
    blog_posts = BlogPost.objects.filter(public=True).order_by('added_on')
    for post in blog_posts:
        post.short_body = post.post_body[:200]
    categories = BlogCategory.objects.all()

    if request.method == 'GET':
        if 'category' in request.GET:
            filter_cat = request.GET['category']
            blog_posts = blog_posts.filter(category__category=filter_cat)
            category = BlogCategory.objects.filter(category=filter_cat)
    
    blog_posts = paginator_helper(request, blog_posts.
                                  order_by('added_on'), 8)
    for post in blog_posts:
        post.short_body = post.post_body[:200]
    template = "blog/blog.html"
    context = {
        'title': 'blog',
        'section': 'blog',
        'blog_posts': blog_posts,
        'categories': categories,
        'category': category,
    }
    return render(request, template, context)


def view_post(request, blog_id):
    """a view to show a full blog post write-up"""
    blog_post = get_object_or_404(BlogPost, pk=blog_id)
    template = "blog/view_post.html"
    context = {
        'title': blog_post.post_title,
        'section': 'blog',
        'blog_post': blog_post,
    }
    return render(request, template, context)
