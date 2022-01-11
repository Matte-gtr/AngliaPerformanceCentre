from django.contrib import admin
from .models import ReviewImage, Review


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewImage)
