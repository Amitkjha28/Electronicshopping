from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from Electronicshopping import settings
from myapp.forms import RegisterForm, LoginForm
from myapp.models import Category, Product, Subcategory, Cart, OrderDetails, Order


def myindex(request):
    # return HttpResponse('<h1> My Shopping App </h1>')
    category_data = Category.objects.all()
    featured_productsdata = Product.objects.filter(featured_product=True)
    product_data = Product.objects.all().order_by('-creation_date')
    return render(request,'index.html',{"categorydata" : category_data,"productdata" : product_data ,"featuredproducts": featured_productsdata})

def mysubcategory(request,cid):
    subcategory_data = Subcategory.objects.filter(category=cid)
    return render(request,'sub_categories.html',{"subcategorydata" : subcategory_data})

def myproduct(request):
    subcategoryid = request.GET.get("subcatid")
    categoryid = request.GET.get("catid")
    product_data = Product.objects.filter(category=categoryid, subcategory=subcategoryid)
    return render(request,'product.html',{"productdata" : product_data})

def myproductdetail(request, pid):
    productdata = Product.objects.get(id=pid)
    return render(request, "product_details.html", {"productdata": productdata})

def mylogin(request):
    return render(request,'login.html')

def mylogin(request):
    myform = LoginForm(request.POST or None)
    if myform.is_valid():
        username = myform.cleaned_data.get("username")
        userobj = User.objects.get(username__iexact=username)
        myredirect_to = request.POST.get('next')
        login(request, userobj)
        request.session['username'] = username
        request.session['name'] = userobj.first_name
        if myredirect_to:
            return redirect(myredirect_to)
        else:
            return HttpResponseRedirect(reverse_lazy("myhome"))
    return render(request, "login.html", {"form": myform})

def mylogout(request):
    if request.session["username"]:
        del request.session["username"]
    if request.session["name"]:
        del request.session["name"]
    logout(request)
    return HttpResponseRedirect(reverse_lazy("myhome"))

class mysignup(SuccessMessageMixin, CreateView):
    form_class = RegisterForm
    template_name = 'signup.html'
    success_url = reverse_lazy('signup')
    success_message = 'Signup Successful. You can login now'

    def dispatch(self, *args, **kwargs):
        return super(mysignup, self).dispatch(*args, **kwargs)

def addtocart(request):
    pid = int(request.POST.get("pid"))
    price = int(float(request.POST.get("price")))
    qty = int(request.POST.get("qty"))
    totalcost = price * qty
    if not request.session or not request.session.session_key:
        request.session.save()
        SESSION_KEY = request.session.session_key
        request.session["sid"] = SESSION_KEY

    cartdata = Cart.objects.filter(productid=pid, sessionid=request.session["sid"]).first()
    if cartdata is not None:
        cartdata.qty = int(cartdata.qty) + qty
        cartdata.totalcost = int(cartdata.price) * cartdata.qty
        Cart.objects.filter(productid=pid, sessionid=request.session["sid"]).update(qty=cartdata.qty,totalcost=cartdata.totalcost)
    else:
        cartobj = Cart()
        cartobj.productid = Product(id=pid)
        cartobj.price = price
        cartobj.qty = qty
        cartobj.totalcost = totalcost
        cartobj.sessionid = request.session["sid"]
        cartobj.save()
    return HttpResponseRedirect(reverse_lazy("showcart"))

@login_required()
def showcart(request):
    if not request.session or not request.session.session_key:
        request.session.save()
        sessionkey =request.session.session_key
        request.session["sid"]=sessionkey
    elif not "sid" in request.session:
        request.session["sid"] = request.session.session_key
    cartdata = Cart.objects.filter(sessionid=request.session["sid"]).select_related("productid")
    cartcount = cartdata.count
    cartsum = Cart.objects.filter(sessionid=request.session["sid"]).aggregate(Sum('totalcost'))
    return render(request, "shopping_cart.html", {"cartdata": cartdata, "cartcount": cartcount, "cartsum": cartsum})

def deletecart(request, id):
    Cart.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse_lazy("showcart"))

@login_required()
def mycheckout(request):
    return render(request, "checkout.html")

def orderdetails(request, oid):
    orderdetailsdata = OrderDetails.objects.filter(orderno=oid)
    return render(request, "orderdetails.html", {"orderdetailsdata": orderdetailsdata})

@login_required()
def myorder(request):
    orderobj = Order()
    name = request.POST.get("name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    email = request.POST.get("email")
    paymentmethod = request.POST.get("paymentmethod")
    orderobj.person_name = name
    orderobj.address = address
    orderobj.phone = phone
    orderobj.email = email
    orderobj.username = User.objects.get(username=request.session["username"])
    orderobj.payment_mode = paymentmethod
    cartsum = Cart.objects.filter(sessionid=request.session["sid"]).aggregate(Sum('totalcost'))

    orderobj.grand_total = cartsum['totalcost__sum']
    orderobj.save()
    orderno = Order.objects.latest('id')


    for cartdata in Cart.objects.filter(sessionid=request.session["sid"]):
        myorderdetailsobj = OrderDetails()
        myorderdetailsobj.orderno = orderno
        myorderdetailsobj.productid = cartdata.productid
        myorderdetailsobj.price = cartdata.price
        myorderdetailsobj.qty = cartdata.qty
        myorderdetailsobj.totalcost = cartdata.totalcost
        myorderdetailsobj.save()

    Cart.objects.filter(sessionid=request.session["sid"]).delete()
    message = EmailMultiAlternatives(
            'New sale at your website',          #Subject
            'You have got a new order',     #Email Body
            to = ['amitjha814631@gmail.com'],  # where you receive the contact emails
            from_email = settings.EMAIL_HOST_USER, reply_to = ['amitjha814631@gmail.com'])
    result = message.send(fail_silently=False)
    return render(request, "thanks.html", {"orderno" : orderno , "result" : result})

@login_required()
def previousorders(request):
    orders = Order.objects.filter(username=User.objects.get(username=request.session["username"])).order_by('-order_date')
    orderscount = orders.count
    return render(request, "previous-orders.html", {"porders" : orders, "orderscount" : orderscount})

def changepassword(request):
    if request.method == "POST":
        oldpassword = request.POST.get("oldpassword", "0")
        newpass1 = request.POST.get("password1", "1")
        newpass2 = request.POST.get("password2", "2")
        if newpass1 == newpass2:
            myusername = request.session["username"]
            userobj = authenticate(username=myusername, password=oldpassword)
            if userobj is not None:
                userobj.set_password(newpass2)
                userobj.save()
                logout(request)
                messages.success(request, 'Password changed successfully. Login again')
                return HttpResponseRedirect(reverse('login'))
            else:
                return render(request, "change_password.html", {"messages": "Wrong old password"})
        else:
            return render(request, "change_password.html", {"messages": "New Passwords does not match"})
    else:
        return render(request, "change_password.html")

def searchproducts(request):
    searchterm = request.GET.get("searchterm")
    products_data = Product.objects.filter(product_name__icontains=searchterm)
    return render(request, "search_results.html", {"productsdata": products_data})

def contactus(request):
    if request.method == "POST":
        name = request.POST.get("Name")
        email = request.POST.get("Email")
        phone = request.POST.get("Phone")
        msg = request.POST.get("Msg")
        mymailbody = "Name : " + str(name) + "\nEmail : " + str(email) + "\nPhone : " + str(phone) + "\nMessage : " + str(msg)
        message = EmailMultiAlternatives(
            'New Message from  Electronic Shopping',  # Subject
             mymailbody,  # Email Body
            to=['amitjha814631@gmail.com'],  # where you receive the contact emails
            from_email=settings.EMAIL_HOST_USER, reply_to=['amitjha814631@gmail.com'])
        message.send(fail_silently=False)
        messages.success(request, 'Thanks for your message. We will contact you shortly')
    return render(request, "contact_us.html")