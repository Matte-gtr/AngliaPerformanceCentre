from django.urls import path
from . import views


urlpatterns = [
    path('', views.blog, name="blog"),
    path('view_post/<int:blog_id>/', views.view_post, name="view_post"),
]
