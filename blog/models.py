from django.db import models


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
    post_body = models.TextField(blank=False)

    def __str__(self):
        return str(self.post_title)


class BlogPostImage(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=False,
                             null=False, related_name="images")
    image = models.ImageField(upload_to="blogs", blank=False, null=False)

    def __str__(self):
        return str(self.pk)
