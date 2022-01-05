from django.urls import path
from . import views


urlpatterns = [
    path('', views.contact, name='contact'),
    path('send_message/', views.send_message, name='send_message'),
    path('callback/', views.send_callback, name='send_callback'),
]
