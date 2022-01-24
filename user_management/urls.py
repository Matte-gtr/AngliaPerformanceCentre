from django.urls import path
from . import views


urlpatterns = [
     path('profile/', views.profile, name="profile"),
     path('admin_messages/', views.admin_messages, name="admin_messages"),
     path('admin_callbacks/', views.admin_callbacks, name="admin_callbacks"),
     path('admin_reviews/', views.admin_reviews, name="admin_reviews"),
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
     path('admin_messages/reply/<int:message_id>', views.reply_to_message,
          name="reply_to_message"),
]
