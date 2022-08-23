from django.contrib import admin
from .models import ProductCategory, DiscountCode, ProductImage, Product, \
    AttributeBase, Attribute, ProductAttribute, ProductReview, \
    ProductReviewImage

admin.site.register(ProductCategory)
admin.site.register(DiscountCode)
admin.site.register(ProductImage)
admin.site.register(Product)
admin.site.register(AttributeBase)
admin.site.register(Attribute)
admin.site.register(ProductAttribute)
admin.site.register(ProductReview)
admin.site.register(ProductReviewImage)
