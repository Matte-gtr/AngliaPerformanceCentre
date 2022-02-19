from django.urls import path
from . import views


urlpatterns = [
     path('', views.blog, name="blog"),
     path('view_post/<int:blog_id>/', views.view_post, name="view_post"),
     path('add_post/', views.add_post, name="add_post"),
     path('post_preview/<int:blog_id>', views.post_preview,
          name="post_preview"),
     path('display_post/<setting>/<int:blog_id>', views.display_post,
          name="display_post"),
     path('delete_blog_post/<next_url>/<int:blog_id>', views.delete_blog_post,
          name="delete_blog_post"),
]
