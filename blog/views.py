from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_management.views import paginator_helper

from .models import BlogPost, BlogCategory, BlogPostVideo
from .forms import BlogPostForm

import re


def clean_snippet(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def blog(request):
    """ a view to display the blog page """
    category = "All"
    filter_cat = None
    blog_posts = BlogPost.objects.filter(publish=True).order_by('-added_on')
    for post in blog_posts:
        post.short_body = post.post_body[:200]
    categories = BlogCategory.objects.all()

    if request.method == 'GET':
        if 'category' in request.GET:
            filter_cat = request.GET['category']
            blog_posts = blog_posts.filter(category__category=filter_cat)
            category = BlogCategory.objects.filter(category=filter_cat)

    blog_posts = paginator_helper(request, blog_posts, 8)
    for post in blog_posts:
        short_body = clean_snippet(post.post_body).replace("&nbsp;", "")
        post.short_body = short_body[:200]
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


@login_required
def add_post(request):
    """ a view to add a new blog post """
    if request.user.is_staff:
        if request.method == "POST":
            form = BlogPostForm(request.POST, request.FILES)
            videos = request.FILES.getlist('video')
            if form.is_valid():
                new_post = form.save()
                for file in videos:
                    vid = BlogPostVideo(video=file)
                    vid.save()
                    new_post.video.add(vid)
                new_post.save()
                return redirect(reverse('post_preview',
                                kwargs={"blog_id": new_post.id}))
            else:
                messages.error(request, "Please check you file upload types \
                               and blog content")
                return redirect(reverse('add_post'))
        else:
            form = BlogPostForm()
            template = "blog/add_post.html"
            context = {
                'title': 'Add Post',
                'section': 'blog',
                'form': form,
            }
            return render(request, template, context)
    else:
        messages.error(request, 'You are not authorised to add Blog posts')
        return redirect(reverse('home'))


@login_required
def post_preview(request, blog_id):
    """ a view to preview a blog post before it is made public """
    if request.user.is_staff:
        blog_post = get_object_or_404(BlogPost, pk=blog_id)
        template = "blog/post_preview.html"
        context = {
            'title': f'Preview {blog_id}',
            'section': 'blog',
            'blog_post': blog_post,
        }
        return render(request, template, context)
    else:
        messages.error(request, "You don't have the required permissions to \
                       view this page")
        return redirect(reverse('blog'))
