from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name="profile"),
    path('admin_panel/', views.admin_panel, name="admin_panel"),
]
