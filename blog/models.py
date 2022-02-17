from django.db import models
from .validators import validate_video_file
from ckeditor_uploader.fields import RichTextUploadingField


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
    post_body = RichTextUploadingField(blank=True, null=True)
    header_image = models.ImageField(upload_to="blogs/header_images",
                                     blank=True, null=True)
    video = models.ManyToManyField('BlogPostVideo', blank=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post_title)


class BlogPostVideo(models.Model):
    video = models.FileField(upload_to="blogs/videos", blank=False, null=False,
                             validators=[validate_video_file])
    filetype = models.CharField(max_length=24, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.filetype:
            self.filetype = self.video.name.split(".")[1]
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)
