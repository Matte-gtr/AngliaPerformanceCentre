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
    image = models.ManyToManyField('BlogPostImage', blank=True)
    video = models.ManyToManyField('BlogPostVideo', blank=True)
    public = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post_title)


class BlogPostImage(models.Model):
    image = models.ImageField(upload_to="blogs", blank=False, null=False)

    def __str__(self):
        return str(self.pk)


class BlogPostVideo(models.Model):
    video = models.FileField(upload_to="blogs", blank=False, null=False,
                             validators=[validate_video_file])

    def __str__(self):
        return str(self.pk)
