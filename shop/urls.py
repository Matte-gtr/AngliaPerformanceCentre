from django.urls import path
from . import views


urlpatterns = [
     path('cars/', views.cars, name="cars"),
     path('parts/', views.parts, name="parts"),
     path('parts/product_detail/<int:product_id>', views.product_detail,
          name="product_detail"),
     path('parts/add_product/', views.add_product, name="add_product"),
     path('parts/delete_product/<int:product_id>', views.delete_product,
          name="delete_product"),
     path('parts/edit_product/<int:product_id>', views.edit_product,
          name="edit_product"),
]
