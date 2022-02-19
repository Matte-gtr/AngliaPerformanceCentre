from django.urls import path
from . import views


urlpatterns = [
     path('profile/', views.profile, name="profile"),
     path('admin_messages/', views.admin_messages, name="admin_messages"),
     path('admin_callbacks/', views.admin_callbacks, name="admin_callbacks"),
     path('admin_reviews/', views.admin_reviews, name="admin_reviews"),
     path('admin_blog_posts/', views.admin_blog_posts, name="admin_blog_posts"),
     path('admin_messages/<int:message_id>', views.view_message,
          name="view_message"),
     path('admin_callbacks/<int:callback_id>', views.view_callback,
          name="view_callback"),
     path('admin_reviews/<int:review_id>', views.view_review,
          name="view_review"),
     path('admin_reviews/approve/<int:review_id>', views.approve_review,
          name="approve_review"),
     path('admin_<model>/unread/<int:object_id>', views.mark_unread,
          name="mark_unread"),
     path('admin_<model>/responded/<int:object_id>', views.toggle_responded,
          name="toggle_responded"),
     path('admin_messages/reply/<int:message_id>', views.reply_to_message,
          name="reply_to_message"),
     path('admin_messages/delete/<int:message_id>', views.delete_message,
          name="delete_message"),
     path('admin_callbacks/delete/<int:callback_id>', views.delete_callback,
          name="delete_callback"),
]
