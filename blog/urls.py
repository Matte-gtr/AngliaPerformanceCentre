from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.blog, name="blog"),
    path('view_post/<int:blog_id>/', views.view_post, name="view_post"),
    path('add_post/', views.add_post, name="add_post"),
    path('post_preview/<int:blog_id>', views.post_preview, name="post_preview"),
]
