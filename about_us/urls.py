from django.urls import path
from . import views


urlpatterns = [
    path('', views.about_us, name="about_us"),
    path('the_team/', views.the_team, name="the_team"),
    path('terms_and_conditions/', views.terms_and_conditions,
         name="terms_and_conditions"),
]
