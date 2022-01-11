from django.urls import path
from . import views


urlpatterns = [
    path('', views.testimonials, name="testimonials"),
    path('review/post/', views.post_review, name="post_review"),
]
