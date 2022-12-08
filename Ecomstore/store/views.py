from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'index.html', context)

def cart(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'cart.html', context)

def checkout(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'checkout.html', context)

def about(request):
    return render(request, 'about.html')

def products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'products.html', context)