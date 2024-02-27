from django.urls import path
from . import views

urlpatterns = [
	path('', views.cart_summary, name="cart_summary"),
	path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('quantity/', views.cart_quantity, name='cart_quantity'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
	# path('delete/', views.cart_delete, name="cart_delete"),
	# path('update/', views.cart_update, name="cart_update"),
]
