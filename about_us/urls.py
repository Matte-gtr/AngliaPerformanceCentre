from django.urls import path
from . import views


urlpatterns = [
    path('', views.about_us, name="about_us"),
    path('the_team/', views.the_team, name="the_team"),
    path('terms_and_conditions/', views.terms_and_conditions,
         name="terms_and_conditions"),
    path('add_team_member/', views.add_team_member, name='add_team_member'),
    path('edit_team_member/<int:member_id>', views.edit_team_member,
         name='edit_team_member'),
    path('delete_team_member/<int:member_id>', views.delete_team_member,
         name='delete_team_member'),
]
