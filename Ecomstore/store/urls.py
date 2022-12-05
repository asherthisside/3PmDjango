from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    # path('product/<int:id>', views.product, name='product'),
    path('products', views.products, name='products'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
]

# Idea - ? 