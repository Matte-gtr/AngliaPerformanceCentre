from django.contrib import admin
from .models import ReviewImages, Review


class ReviewImagesInline(admin.StackedInline):
    model = ReviewImages


class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImagesInline]


admin.site.register(Review, ReviewAdmin)
