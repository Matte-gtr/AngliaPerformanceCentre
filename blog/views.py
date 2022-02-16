from django.shortcuts import render
from .models import BlogPost, BlogCategory
from user_management.views import paginator_helper


def blog(request):
    """ a view to display the blog page """
    category = "All"
    filter_cat = None
    blog_posts = BlogPost.objects.all().order_by('added_on')
    for post in blog_posts:
        post.short_body = post.post_body[:200]
    categories = BlogCategory.objects.all()

    if request.method == 'GET':
        if 'category' in request.GET:
            filter_cat = request.GET['category']
            blog_posts = blog_posts.filter(category__category=filter_cat)
            category = request.GET['category']
    
    blog_posts = paginator_helper(request, blog_posts.
                                  order_by('added_on'), 8)
    template = "blog/blog.html"
    context = {
        'title': 'blog',
        'section': 'blog',
        'blog_posts': blog_posts,
        'categories': categories,
        'filter_cats': filter_cat,
        'category': category,
    }
    return render(request, template, context)
