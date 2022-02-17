from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.blog, name="blog"),
    path('view_post/<int:blog_id>/', views.view_post, name="view_post"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
