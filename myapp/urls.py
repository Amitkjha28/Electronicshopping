from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Electronicshopping import settings
from myapp import views
urlpatterns = [
    # path('', views.myindex),
    path('', views.myindex,name='myhome'),
    path('user_login',views.mylogin,name='login' ),
    path('user-logout', views.mylogout, name='logout'),
    path('user_signup',views.mysignup.as_view(),name='signup' ),
    path('subcat/<int:cid>',views.mysubcategory,name='subcategory' ),
    path('product',views.myproduct,name='product'),
    path('product_detail/<int:pid>', views.myproductdetail, name='productdetail'),
    path('add_cart', views.addtocart, name='addtocart'),
    path('shopping_cart', views.showcart, name='showcart'),
    path('delete_cart/<int:id>', views.deletecart, name='deletecart'),
    path('user_checkout', views.mycheckout, name='checkout'),
    path('order_success', views.myorder, name='order'),
    path('order_details/<int:oid>', views.orderdetails, name='orderdetails'),
    path('my_orders', views.previousorders, name='previousorders'),
    path('My_pass_change', views.changepassword, name='changepass'),
    path('search/results', views.searchproducts, name='searchproduct'),
    path('contact/us', views.contactus, name='contact'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)





