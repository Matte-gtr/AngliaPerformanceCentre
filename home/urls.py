from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('add_advert/', views.add_advert, name="add_advert"),
    path('edit_advert/<int:advert_id>', views.edit_advert, name="edit_advert"),
    path('delete_advert/<int:advert_id>', views.delete_advert, name="delete_advert"),
]
