import random
import string
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Order
from django.db.models import Q
import razorpay
from django.core.mail import send_mail

context={}
categories = Product.CAT
context['categories']=categories
p=Product.objects.filter(is_active=True)
context['products']=p
# Create your views here.
def about(request):
    return HttpResponse("This is About page")

def contact(request):
    return HttpResponse("This is Contact page")

def delete(request, rid):
    print("ID to be deleted: ", rid)
    return HttpResponse("ID to be deleted: " + rid)

def addition(request, x,y):
    a=int(x)+int(y)
    #print("Addition is: ", a)
    return HttpResponse("Addition is: " + str(a))

class SimpleView(View):
    def get(self, request):
        return HttpResponse("Hello from class view!!")
    
def hello(request):
    context={}
    context['greet']="Good evening, we are learning DTL"
    context['x']=120
    context['y']=100
    context['l']=[10,20,30,40,50,60]
    context['products']=[
        {'id':1,'name':'samsung','cat':'mobile','price':15000},
        {'id':2,'name':'jeans','cat':'clothes','price':800},
        {'id':3,'name':'adidas','cat':'shoes','price':2200},
        {'id':4,'name':'vivo','cat':'mobile','price':16000},
    ]
    return render(request,'hello.html',context)

def home(request):
    # userid=request.user.id
    # print("Logged-in UserId is: ", userid)
    # print(request.user.is_authenticated)
    # context={}
    p=Product.objects.filter(is_active=True)
    # print(p)
    context['products']=p
    return render(request,'index.html',context)

def product(request,pid):
    p=Product.objects.get(id=pid)
    context['products']=p
    keys_to_remove = ['success', 'errmsg']
    for key in keys_to_remove:
        context.pop(key, None) 
    return render(request, 'product.html', context)

def register(request):
    if request.method == 'POST':
        uemail = request.POST['uemail']
        upass = request.POST['upass']
        cpass = request.POST['cpass']
        context={}
        if uemail == "" or upass == "" or cpass == "":
            context['errmsg'] = "Fields cannot be empty"
        elif upass != cpass:
            context['errmsg'] = "Password and Confirm password didn't match...!!!"
        else:
            try:
                u=User.objects.create(password=upass,username=uemail,email=uemail)
                u.set_password(upass)
                u.save()
                context['success'] = "User created sucessfully"
            except:
                context['errmsg'] = "Username already exists...!!!"
        return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')
    
def user_login(request):
    if request.method == 'POST':
         uemail = request.POST['uemail']
         upass = request.POST['upass']
         context={}
         if uemail == "" or upass == "":
            context['errmsg'] = "Fields cannot be empty"
            return render(request, 'login.html', context)
         else:
             u=authenticate(username=uemail,password=upass)
             if u is not None:
                 login(request,u)
                 return redirect('/')
             else:
                 context['errmsg'] = "Invalid username and password"
                 return render(request, 'login.html', context)
            #  print(u)
            #  print(u.is_superuser)
            #  print(u.email)
            #  return HttpResponse('Data fetched')
    else:
        return render(request, 'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    #categories = Product.CAT
    #print(p)
    # context={}
    context['products']=p
    # return render(request, 'index.html', {'products': p, 'categories': categories})
    return render(request,'index.html', context)

def sort(request,sv):
    if sv == '0':
        col='price'
    else:
        #descending
        col='-price'
    p=Product.objects.filter(is_active=True).order_by(col)
    # context={}
    context['products']=p
    # return render(request, 'index.html', {'products': p, 'categories': categories})
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context['products']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if(request.user.is_authenticated):
        userid=request.user.id
        u=User.objects.get(id=userid)
        p=Product.objects.get(id=pid)
        context['products']=p
        keys_to_remove = ['success', 'errmsg']
        for key in keys_to_remove:
            context.pop(key, None) 
        #Check product exists or not
        q1=Q(uid=u)
        q2=Q(pid=p)
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==1:
            context['errmsg'] = "Product already exists in cart!!!"
        else:
            c=Cart.objects.create(uid=u,pid=p)
            c.save()
            context['success'] = "Product added sucessfully"
        return render(request,'product.html',context)
    else:
        return redirect('/login')

def viewcart(request):
    keys_to_remove = ['success', 'errmsg']
    for key in keys_to_remove:
        context.pop(key, None) 
    c=Cart.objects.filter(uid=request.user.id)
    n=len(c)
    total_price = sum(item.pid.price*item.qty for item in c)
    context['product_count']=n
    context['total_price']=total_price
    context['products']=c
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,cid,qv):
    c=Cart.objects.get(id=cid)
    if qv == '1':
        c.qty += 1
    elif qv == '0' and c.qty > 1:
        c.qty -= 1
    else:
        c.qty = 1
    c.save()
    return redirect('/viewcart')

def placeorder(request):
    keys_to_remove = ['success', 'errmsg']
    for key in keys_to_remove:
        context.pop(key, None) 
    c=Cart.objects.filter(uid=request.user.id)
    #oid=random.randrange(1000,9999)
    order_id = generate_order_id()
    for x in c:
        o=Order.objects.create(order_id=order_id,uid=x.uid,pid=x.pid,qty=x.qty)
        o.save()
        x.delete()
    o=Order.objects.filter(uid=request.user.id)
    n=len(o)
    total_price = sum(item.pid.price*item.qty for item in o)
    context['product_count']=n
    context['total_price']=total_price
    context['orders']=o
    return render(request,'placeorder.html',context)

def generate_order_id(length=10):
    # Define the characters: uppercase letters and digits
    characters = string.ascii_uppercase + string.digits
    # Generate a random alphanumeric string
    order_id = ''.join(random.choices(characters, k=length))
    return order_id

def removeorder(request,oid):
    o=Order.objects.filter(id=oid)
    o.delete()
    return redirect('/placeorder')

def makepayment(request):    
    o=Order.objects.filter(uid=request.user.id)
    n=len(o)
    print(n)
    order_id = o[n-1].order_id
    total_price = o[n-1].pid.price*o[n-1].qty
    
    # total_price = sum(item.pid.price*item.qty for item in o)
    client = razorpay.Client(auth=("rzp_test_pjmfONoAV5hhRJ", "2qLFlWxOv0vaA1jxWEEHwbcA"))
    data = { "amount": total_price*100, "currency": "INR", "receipt": order_id }
    payment = client.order.create(data=data)
    #print(payment)
    context['data']=payment
    #return HttpResponse("Success")
    return render(request, 'pay.html', context)

def sendusermail(request):
    uemail=request.user.email
    #print(uemail)
    #msg= "Order details are: \n Order ID- " + response.razorpay_order_id + "\n Payment ID- " + response.razorpay_payment_id + "Signature-"+response.razorpay_signature
    send_mail(
        "Estore order placed successfully",
        "Order details are:",
        "soniyakamble.09@gmail.com",
        [uemail],
        fail_silently=False,
    )
    return HttpResponse("Mail sent successfully")

# def placeorder(request):
#     keys_to_remove = ['success', 'errmsg']
#     for key in keys_to_remove:
#         context.pop(key, None) 
#     o=Order.objects.filter(uid=request.user.id)
#     n=len(o)
#     total_price = sum(item.pid.price for item in o)
#     context['product_count']=n
#     context['total_price']=total_price
#     context['orders']=o
#     return render(request,'cart.html',context)