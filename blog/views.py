from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_management.views import paginator_helper

from .models import BlogPost, BlogCategory, BlogPostVideo
from .forms import BlogPostForm

import re
from datetime import datetime


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
                    vid.full_clean()
                    vid.save()
                    new_post.video.add(vid)
                new_post.save()
                return redirect(reverse('post_preview',
                                kwargs={"blog_id": new_post.id}))
            else:
                messages.error(request, "Please check you file upload types \
                               and blog content")
        else:
            form = BlogPostForm()
    else:
        messages.error(request, 'You are not authorised to add Blog posts')
        return redirect(reverse('home'))
    template = "blog/add_post.html"
    context = {
        'title': 'Add Post',
        'section': 'blog',
        'form': form,
    }
    return render(request, template, context)



@login_required
def post_preview(request, blog_id):
    """ a view to preview a blog post before it is made public """
    if request.user.is_staff:
        blog_post = get_object_or_404(BlogPost, pk=blog_id)
        refer = request.META.get('HTTP_REFERER')
        refer = refer.split('/')[-2]
        if blog_post.publish == True:
            messages.error(request, f"Blog post {blog_id} is already \
                published")
            return redirect(reverse('blog'))
    else:
        messages.error(request, "You don't have the required permissions to \
                       view this page")
        return redirect(reverse('blog'))
    template = "blog/post_preview.html"
    context = {
        'title': f'Preview {blog_id}',
        'section': 'blog',
        'blog_post': blog_post,
        'refer': refer,
    }
    return render(request, template, context)


@login_required
def display_post(request, blog_id, setting):
    """ a view to publish a blog post to the blog """
    if request.user.is_staff:
        blog_post = get_object_or_404(BlogPost, pk=blog_id)
        blog_post.publish = setting
        blog_post.save(update_fields={'publish'})
        if setting == "True":
            messages.success(request, "Your post has been published on the \
                            Blog page")
        else:
            messages.success(request, "Your post has been removed from the \
                            Blog page")
        return redirect(reverse('blog'))
    else:
        messages.error(request, "You don't have the required permissions \
                       to complete this action")
        return redirect(reverse('blog'))


@login_required
def delete_blog_post(request, blog_id, next_url="blog"):
    """ a view to delete a blog post """
    blog_post = get_object_or_404(BlogPost, pk=blog_id)
    if request.user.is_staff:
        videos = blog_post.video.all()
        try:
            if videos:
                for item in videos:
                    video = get_object_or_404(BlogPostVideo, pk=item.pk)
                    try:
                        video.delete()
                    except Exception as e:
                        messages.error(request, f"error deleting image: {e}")
            blog_post.delete()
            messages.success(request, f"Blog post {blog_id} successfully deleted")
        except Exception as e:
            messages.error(request, f"error deleting blog post: {e}")
    else:
        messages.error(request, "You don't have the required permission \
                       to complete this action")
        return redirect(reverse('blog'))
    return redirect(reverse(next_url))


@login_required
def edit_blog_post(request, blog_id):
    """ a view to edit a blog post """
    blog_post = get_object_or_404(BlogPost, pk=blog_id)
    if request.user.is_staff:
        if request.method == "POST":
            form = BlogPostForm(request.POST, request.FILES,
                                instance=blog_post)
            files = request.FILES.getlist('video')
            if form.is_valid():
                delete_string = request.POST.get('videocontrol')
                delete_list = []
                if delete_string:
                    delete_list = delete_string.split(",")
                if delete_list:
                    for video_id in delete_list:
                        blog_video = get_object_or_404(BlogPostVideo,
                                                       pk=video_id)
                        try:
                            blog_video.delete()
                        except Exception as e:
                            messages.error(request, f"error deleting \
                                           video: {e}")
                form_blog_post = form.save(commit=False)
                form_blog_post.added_on = datetime.now()
                form_blog_post.save()
                for file in files:
                    vid = BlogPostVideo(video=file)
                    vid.full_clean()
                    vid.save()
                    blog_post.video.add(vid)
                form.save()
                messages.success(request, "Your Post has been \
                                successfully updated.")
                return redirect(reverse('post_preview',
                                        args={blog_id: blog_id}))
            else:
                messages.error(request, "Update failed, Please ensure all fields \
                                are filled in correctly")
        else:
            form = BlogPostForm(instance=blog_post)
    else:
        messages.warning(request, "You don't have the required \
                         permissions to edit blog posts")
        return redirect(reverse('blog'))
    template = "blog/edit_blog_post.html"
    context = {
        'title': f"Edit Post {blog_id}",
        'section': 'blog',
        'blog_post': blog_post,
        'form': form,
    }
    return render(request, template, context)
