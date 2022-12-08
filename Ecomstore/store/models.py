from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=35)
    address = models.CharField(max_length=200)
    email = models.CharField(max_length=65)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=35)
    discount = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def productnum(self):
        prods = self.product_set.all()
        num = prods.count()
        return num 

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    description = models.TextField()
    digital = models.BooleanField()
    image = models.ImageField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url 
        except:
            url = ""
        return url

    def __str__(self):
        return self.name + " - " + str(self.category)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.id) + " - " + self.customer.name + " " + str(self.date_ordered)

    @property
    def cart_total(self):
        items = self.orderitem_set.all()
        cart_total = sum([item.itemsprice for item in items])
        return cart_total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + " - " + self.order.customer.name + " - " + str(self.order.id) + " - " + self.product.name + " (" + str(self.quantity) + ")"

    @property
    def itemsprice(self):
        return self.product.price * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.name + " - " + self.address