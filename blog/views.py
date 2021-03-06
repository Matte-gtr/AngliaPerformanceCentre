import re
import json
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from user_management.views import paginator_helper

from .models import BlogPost, BlogCategory, BlogPostVideo, BlogPostComment
from .forms import BlogPostForm


def clean_snippet(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def blog(request):
    """ a view to display the blog page """
    category = "All"
    searched = None
    filter_cat = None
    blog_posts = BlogPost.objects.filter(publish=True).order_by('-added_on')
    for post in blog_posts:
        post.short_body = post.post_body[:200]
    categories = BlogCategory.objects.all()

    if request.method == 'GET':
        if 'category' in request.GET:
            filter_cat = request.GET.get('category')
            blog_posts = blog_posts.filter(category__category=filter_cat)
            category = BlogCategory.objects.filter(category=filter_cat)

        if 'search' in request.GET:
            searched = request.GET.get('search')
            blog_posts = blog_posts.filter(
                Q(post_body__icontains=searched) |
                Q(post_title__icontains=searched) |
                Q(category__friendly_name__icontains=searched)
                )

    blog_posts = paginator_helper(request, blog_posts, 8)
    for post in blog_posts:
        short_body = clean_snippet(post.post_body).replace("&nbsp;", "")
        post.short_body = short_body[:200]
    if not category == "All":
        param_title = category[0]
    else:
        param_title = None
    template = "blog/blog.html"
    context = {
        'title': 'blog',
        'section': 'blog',
        'blog_posts': blog_posts,
        'categories': categories,
        'category': category,
        'param_title': param_title,
        'searched': searched,
    }
    return render(request, template, context)


def view_post(request, blog_id):
    """a view to show a full blog post write-up"""
    blog_post = get_object_or_404(BlogPost, pk=blog_id)
    if not blog_post.publish:
        messages.error(request, f"Post {blog_id} has not been published")
        return redirect(reverse('blog'))
    short_body = clean_snippet(blog_post.post_body).replace("&nbsp;", "")
    youtube_clip = ""
    if blog_post.youtube_link:
        youtube_clip = blog_post.youtube_link.split('=')[-1]
    template = "blog/view_post.html"
    context = {
        'title': blog_post.post_title,
        'section': 'blog',
        'blog_post': blog_post,
        'short_body': short_body,
        'youtube_clip': youtube_clip,
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
            messages.error(request, "Please check your file upload types \
                            and blog content")
        else:
            form = BlogPostForm()
    else:
        messages.warning(request, 'You are not authorised to add Blog posts')
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
        youtube_clip = ""
        if blog_post.youtube_link:
            youtube_clip = blog_post.youtube_link.split('=')[-1]
        if blog_post.publish is True:
            messages.info(request, f"Blog post {blog_id} is already \
                published")
            return redirect(reverse('blog'))
    else:
        messages.warning(request, "You don't have the required permissions to \
                       view this page")
        return redirect(reverse('blog'))
    template = "blog/post_preview.html"
    context = {
        'title': f'Preview {blog_id}',
        'section': 'blog',
        'blog_post': blog_post,
        'refer': refer,
        'youtube_clip': youtube_clip,
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
    messages.warning(request, "You don't have the required permissions \
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
                    except Exception as err:
                        messages.error(request, f"error deleting blog \
                            video: {err}")
            blog_post.delete()
            messages.success(request, f"Blog post {blog_id} successfully \
                deleted")
        except Exception as err:
            messages.error(request, f"error deleting blog post: {err}")
    else:
        messages.warning(request, "You don't have the required permission \
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
                        except Exception as err:
                            messages.error(request, f"error deleting \
                                           video: {err}")
                form_blog_post = form.save(commit=False)
                form_blog_post.added_on = datetime.now()
                form_blog_post.save()
                for file in files:
                    vid = BlogPostVideo(video=file)
                    vid.full_clean()
                    vid.save()
                    blog_post.video.add(vid)
                form.save()
                messages.success(request, "Blog post updated successfully")
                return redirect(reverse('post_preview',
                                        args={blog_id: blog_id}))
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


@login_required
def post_comment(request, blog_id):
    """ post a comment on a blog post via ajax """
    if request.is_ajax():
        if request.user.is_authenticated:
            blog_post = get_object_or_404(BlogPost, pk=blog_id)
            comment = request.POST.get('comment')
            user_obj = get_object_or_404(User, pk=request.user.pk)
            username = user_obj.username
            newblog = BlogPostComment.objects.create(
                    blogpost=blog_post,
                    user=user_obj,
                    comment=comment
            )
            date = newblog.date_added.strftime("%B %d, %Y, %I:%M %p")
            data = {}
            data['comment'] = comment
            data['user'] = username
            data['date'] = date
            data['comment_id'] = newblog.id
            return JsonResponse(data)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            return redirect(reverse('view_post', kwargs={'blog_id': blog_id}))           
    return redirect(reverse('view_post', kwargs={'blog_id': blog_id}))


@login_required
def delete_comment(request, blog_id):
    """ delete a comment on a blog post via ajax """
    if request.is_ajax():
        if request.user.is_authenticated:
            user = get_object_or_404(User, pk=request.user.pk)
            if user.is_authenticated:
                comment_id = request.POST.get('comment_id')
                comment = get_object_or_404(BlogPostComment, pk=comment_id)
                data = {}
                if user.username == comment.user.username or user.is_staff:
                    comment.delete()
                    status = 'update'
                else:
                    messages.error(request, "You can't delete other users \
                                   comments")
                    status = 'reload'
                data['comment_id'] = comment_id
                data['status'] = status
                return JsonResponse(data)
    return redirect(reverse('view_post', kwargs={'blog_id': blog_id}))


@login_required
def like_unlike_post(request, blog_id):
    """ view to like or unlike a blog post """
    if request.is_ajax():
        user = get_object_or_404(User, pk=request.user.id)
        blog_post = get_object_or_404(BlogPost, pk=blog_id)
        if user.is_authenticated:
            if user in blog_post.likes.all():
                blog_post.likes.remove(user)
                status = 'dislike'
            else:
                blog_post.likes.add(user)
                status = 'like'
            blog_post.save()
            data = {}
            data['status'] = status
            return JsonResponse(data)
    return redirect(reverse('view_post', kwargs={'blog_id': blog_id}))
