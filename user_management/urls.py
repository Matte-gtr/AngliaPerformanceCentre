from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('admin_panel/', views.admin_panel, name="admin_panel"),
    path('admin_panel/view_message/<int:message_id>', views.view_message,
         name="view_message"),
    path('admin_panel/view_review/<int:review_id>', views.view_review,
         name="view_review"),
    path('admin_panel/view_callback/<int:callback_id>', views.view_callback,
         name="view_callback"),
]
