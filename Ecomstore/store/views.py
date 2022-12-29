from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.


def index(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)
        ordereditems = OrderItem.objects.filter(order=order)
        item_count = sum(item.quantity for item in ordereditems)
    else:
        item_count = 0
        ordereditems = []
        order = {"cart_total": 0}
    context = {
        'categories': categories,
        'items': ordereditems,
        'count': item_count,
        'order': order
    }
    return render(request, 'index.html', context)


def cart(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)
        ordereditems = OrderItem.objects.filter(order=order)
        item_count = sum(item.quantity for item in ordereditems)
    else:
        item_count = 0
        ordereditems = []
        order = {"cart_total": 0}
    if request.method == 'POST':
        quantity = request.POST['quantity']
        print(quantity)
    context = {
        'categories': categories,
        'items': ordereditems,
        'count': item_count,
        'order': order
    }
    return render(request, 'cart.html', context)


def checkout(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
        customer=request.user.customer, complete=False)
        ordereditems = OrderItem.objects.filter(order=order)
    else:
        item_count = 0
        ordereditems = []
        order = {"cart_total": 0}
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

        new_shipping = ShippingAddress(
            customer=request.user.customer, order=order, address=address, city=city, state=state, zipcode=zip)
        new_shipping.save()
        order.complete = True

        messages.success(request, "Order has been placed")
        return redirect("products")

    else:
        item_count = sum(item.quantity for item in ordereditems)
        context = {
            'categories': categories,
            'items': ordereditems,
            'count': item_count,
            'order': order
        }
        return render(request, 'checkout.html', context)


def about(request):
    return render(request, 'about.html')


def products(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        p_name = request.POST['product']
        products = Product.objects.filter(name__contains=p_name)
    else:
        products = Product.objects.all()
    if request.user.is_authenticated: 
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)
        ordereditems = OrderItem.objects.filter(order=order)
        item_count = sum(item.quantity for item in ordereditems)
    else:
        item_count = 0
        ordereditems = []
        order = {"cart_total": 0}
    context = {
        'order': order,
        'categories': categories,
        'count': item_count,
        'items': ordereditems,
        'products': products
    }
    return render(request, 'products.html', context)


def product(request, id):
    order, created = Order.objects.get_or_create(
        customer=request.user.customer, complete=False)
    ordereditems = OrderItem.objects.filter(order=order)
    item_count = sum(item.quantity for item in ordereditems)
    product = Product.objects.get(id=id)
    selected_item = order.orderitem_set.get(product=product)
    context = {
        'count': item_count,
        'items': ordereditems,
        'product': product,
        'selected_item': selected_item,
    }
    return render(request, 'single_product.html', context)


def cat_product(request, cid):
    categories = Category.objects.all()
    category = Category.objects.get(id=cid)
    order, created = Order.objects.get_or_create(
        customer=request.user.customer, complete=False)
    ordereditems = OrderItem.objects.filter(order=order)
    item_count = sum(item.quantity for item in ordereditems)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'count': item_count,
        'items': ordereditems,
        'products': products
    }
    return render(request, 'category.html', context)


def add_to_cart(request, pid):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    product = Product.objects.get(id=pid)
    try: 
        cart_item = OrderItem.objects.get(product=product, order=order)
        cart_item.quantity += 1 
        cart_item.save()
    except OrderItem.DoesNotExist:
        cart_item = OrderItem.objects.create(
            product=product, 
            order=order, 
            quantity=1
        )
        cart_item.save()
    return redirect("/products")

def sort(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    ordereditems = OrderItem.objects.filter(order=order)
    item_count = sum(item.quantity for item in ordereditems)
    if request.method == 'POST':
        sortby = request.POST['sortby']

        if sortby == 'pricel2h':
            products = Product.objects.order_by("price")   

        if sortby == 'priceh2l':
            products = Product.objects.order_by("-price") 

    context = {
        'count': item_count,
        'items': ordereditems,
        'products': products,
        'categories': categories,
    }
    return render(request, 'sortedproducts.html', context)
    
def quanminus(request, pid ):
    customer = request.user.customer
    order = Order.objects.get(customer=customer, complete=False)
    item = order.orderitem_set.get(id=pid)
    item.quantity -= 1 
    item.save()
    if item.quantity < 1:
        item.delete()
    return redirect("/cart")

def quanplus(request, pid):
    customer = request.user.customer
    order = Order.objects.get(customer=customer, complete=False)
    item = order.orderitem_set.get(id=pid)  
    item.quantity += 1 
    item.save()
    return redirect("/cart") 
# https://github.com/Sandyrepo8650/Ecom
