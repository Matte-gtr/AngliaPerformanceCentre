from django.contrib import admin
from .models import ReviewImage, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'pk',
        'stars',
        'created_on',
    ]


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewImage)
