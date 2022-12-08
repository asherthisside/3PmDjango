from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'index.html', context)

def cart(request):
    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    ordereditems = OrderItem.objects.filter(order=order)
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'items': ordereditems,
        'order': order
    }
    return render(request, 'cart.html', context)

def checkout(request):
    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    ordereditems = OrderItem.objects.filter(order=order)
    categories = Category.objects.all()
    if request.method == "POST":
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        if address2:
            address = address1 + address2
        else:
            address = address1
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']

        new_shipping = ShippingAddress(customer=request.user.customer, order=order, address=address, city=city, state=state, zipcode=zip)
        new_shipping.save()
        order.complete = True
        
        messages.success(request, "Order has been placed")
        return redirect("products") 

    else:
        context = {
            'categories': categories,
            'items': ordereditems,
            'order': order
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