from django.urls import path
from . import views


urlpatterns = [
    path('', views.testimonials, name="testimonials"),
    path('review/post/', views.post_review, name="post_review"),
    path('review/delete/<int:review_id>', views.delete_review, name="delete_review"),
    path('review/edit/<int:review_id>', views.edit_review, name="edit_review"),
]
