from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from .validators import validate_video_file
from testimonials.models import compress

from django.contrib.auth.models import User


class BlogCategory(models.Model):
    category = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254)

    class Meta:
        verbose_name_plural = 'Blog_Categories'
        ordering = ['id']

    def __str__(self):
        return str(self.friendly_name)


class BlogPost(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE,
                                 blank=False, null=False,
                                 related_name="blog_posts")
    post_title = models.CharField(max_length=254, blank=False, null=False)
    added_on = models.DateTimeField(auto_now_add=True)
    post_body = RichTextUploadingField(blank=False, null=False)
    header_image = models.ImageField(upload_to="blogs/header_images",
                                     blank=True, null=True)
    video = models.ManyToManyField('BlogPostVideo', blank=True)
    youtube_link = models.CharField(blank=True, max_length=500)
    publish = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="blog_post")

    def __str__(self):
        return str(self.post_title)

    def save(self, *args, **kwargs):
        if self.header_image:
            if self.header_image.size > (300 * 1024):
                new_image = compress(self.header_image)
                self.header_image = new_image
        super().save(*args, **kwargs)


class BlogPostVideo(models.Model):
    video = models.FileField(upload_to="blogs/videos", blank=True, null=True,
                             validators=[validate_video_file])
    filetype = models.CharField(max_length=24, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.filetype:
            self.filetype = self.video.name.split(".")[1]
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)


class BlogPostComment(models.Model):
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE,
                                 related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return str(self.pk)
