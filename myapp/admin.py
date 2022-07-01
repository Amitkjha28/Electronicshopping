from django.contrib import admin

# Register your models here.

# 1st Method
from myapp.models import Category, Subcategory, Product, OrderDetails, Order

admin.site.register(Category)

#2nd Method
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['subcategory_name','category']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','price','discount_percent','subcategory','category']

@admin.register(Order)
class MyOrder(admin.ModelAdmin):
    list_display = ['id', 'person_name', 'address', 'phone','email', 'grand_total', 'payment_mode', 'order_date', 'username','order_status']

@admin.register(OrderDetails)
class MyOrderDetails(admin.ModelAdmin):
    list_display = ['orderno', 'productid', 'price', 'qty', 'totalcost']