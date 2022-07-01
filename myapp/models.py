from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=60)
    category_Image = models.ImageField(upload_to='categorypics', blank='True', null='True')

    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=50)
    subcategory_Image = models.ImageField(upload_to='subcategorypics', blank='True', null='True')

    def __str__(self):
        return self.subcategory_name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    product_name= models.CharField(max_length=200)
    price = models.IntegerField()
    discount_percent = models.IntegerField(default=0)
    Image1 = models.ImageField(upload_to='productpics',blank='True',null='True')
    Image2 = models.ImageField(upload_to='productpics', blank='True', null='True')
    Image3 = models.ImageField(upload_to='productpics', blank='True', null='True')
    features = RichTextField(null=True, blank=True)
    details = RichTextField(null=True, blank=True)
    featured_product = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name


    @property
    def discountedprice(self):
        if self.discount_percent > 0:
            discounted_price = self.price - (self.price * self.discount_percent) / 100
            return discounted_price
        else:
            return self.price

class Cart(models.Model):
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    price = models.IntegerField()
    totalcost = models.IntegerField()
    sessionid = models.CharField(max_length=200)

class Order(models.Model):
    person_name = models.CharField(max_length=400)
    address = models.TextField()
    phone = models.BigIntegerField()
    email = models.EmailField()
    grand_total = models.IntegerField()
    payment_mode = models.CharField(max_length=500)
    order_date = models.DateTimeField(auto_now_add=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    order_options = (('received','Order Received'),('processing', 'Order in Process'),('shipped', 'Order Shipped'), ('cancelled', 'Order Cancelled'))
    order_status = models.CharField(max_length = 10,choices=order_options, default='received')

    def __str__(self):
        return self.email

class OrderDetails(models.Model):
    orderno = models.ForeignKey(Order, on_delete=models.CASCADE)
    productid = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    qty = models.IntegerField()
    totalcost = models.IntegerField(default=0)

    def __str__(self):
        return self.orderno

