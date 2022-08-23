from PIL import Image
from io import BytesIO

from django.db import models
from django.core.files import File
from django.contrib.auth.models import User

from testimonials.models import compress


def compress_mini(image):
    img = Image.open(image)
    img_io = BytesIO()
    img = img.resize([100, 100])
    img = img.convert("RGB")
    img = img.save(img_io, 'JPEG', quality=30)
    new_image = File(img_io, name=image.name)
    return new_image


class ProductCategory(models.Model):
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        verbose_name_plural = "Product categories"

    def __str__(self):
        return str(self.name)


class DiscountCode(models.Model):
    code = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    discount_percentage = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return str(f'{self.code} - {self.description}')


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product_images",
                              blank=False,
                              null=False)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (100 * 100):
                new_image = compress(self.image)
                self.image = new_image
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL,
                                 blank=False, null=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    product_code = models.CharField(max_length=255, blank=False, null=False)
    make = models.CharField(max_length=255, blank=True)
    model = models.CharField(max_length=255, blank=True)
    manufacturer = models.CharField(max_length=255, blank=False)
    net_price = models.DecimalField(decimal_places=2, max_digits=8,
                                    blank=True)
    price_incl_vat = models.DecimalField(decimal_places=2, max_digits=8,
                                         blank=False)
    vat = models.DecimalField(decimal_places=2, max_digits=8,
                              blank=True)
    discount_code = models.ManyToManyField(DiscountCode, blank=True)
    publish = models.BooleanField(default=False)
    description = models.TextField()
    fitting_cost = models.DecimalField(decimal_places=2, max_digits=8,
                                       blank=True, null=True)
    images = models.ManyToManyField(ProductImage, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        net_price = (self.price_incl_vat / 120) * 100
        vat = self.price_incl_vat - net_price
        self.net_price = net_price
        self.vat = vat
        super().save(*args, **kwargs)


class AttributeBase(models.Model):
    label = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return str(self.label)


class Attribute(models.Model):
    base = models.ForeignKey(AttributeBase,
                             on_delete=models.CASCADE,
                             related_name="attributes")
    value = models.CharField(max_length=255)
    internal_value = models.CharField(max_length=255,
                                      blank=True)
    image_clip = models.ImageField(upload_to="product_attributes",
                                   blank=True,
                                   null=True)

    def __str__(self):
        return str(self.value)

    def save(self, *args, **kwargs):
        if self.image_clip:
            if self.image_clip.size > (100 * 100):
                new_image = compress_mini(self.image_clip)
                self.image_clip = new_image
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name="attributes",
                                on_delete=models.CASCADE)
    attr = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    additional_cost = models.DecimalField(decimal_places=2, max_digits=6,
                                          blank=True)

    def __str__(self):
        return str(self.pk)


class ProductReview(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    STAR_CHOICES = (
        ('', 'Select'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(User, related_name='product_reviews',
                             on_delete=models.RESTRICT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    stars = models.IntegerField(default='', choices=STAR_CHOICES, blank=False)
    review = models.TextField(blank=False)
    image = models.ManyToManyField('ProductReviewImage', blank=True)
    anon = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class ProductReviewImage(models.Model):
    image = models.ImageField(upload_to="reviews", blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (300 * 1024):
                new_image = compress(self.image)
                self.image = new_image
        super().save(*args, **kwargs)
