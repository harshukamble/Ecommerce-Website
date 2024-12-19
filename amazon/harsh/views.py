from django.shortcuts import render, redirect
from .forms import Re_form, Customer_form
from django.contrib import messages
from django.contrib.auth import logout
from .models import Customer,Product,Cart,Orders
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    mobile=Product.objects.filter(category='mobile')
    laptop=Product.objects.filter(category='laptop')
    if request.user.is_authenticated:
        try:
            fname=Customer.objects.get(customer=request.user)
            name=fname.Full_name
        except Customer.DoesNotExist:
            name='guest'
        return render(request, 'harsh/home.html',{'name':name,'mobile':mobile,'laptop':laptop})
    else:
        return render(request, 'harsh/home.html',{'mobile':mobile,'laptop':laptop})
def signup(request):
    if request.method=='POST':
        context=Re_form(request.POST)
        if context.is_valid():
            context.save()
            messages.success(request, "registred successfully!!")
        else:
            messages.error(request, "registred unsuccessfully!!")
    else:
        context=Re_form()
    return render(request, 'harsh/signup.html', {'context':context})
def user_logout(request):
    logout(request)
    return redirect('login')
def customer_details(request):
    check_temp=Customer.objects.filter(customer=request.user)
    if check_temp.exists():
        return redirect('home')
    if request.method=='POST':
        context=Customer_form(request.POST)
        if context.is_valid():
            temp=context.save(commit=False)
            temp.customer=request.user
            existing_customer=Customer.objects.filter(customer=request.user)
            if existing_customer.exists():
                messages.error(request, "allready added!!")
                return redirect('home') 
            else:
                temp.save()
                messages.success(request, "customer details added Successfuully!!!")
                return redirect('home')
        else:
            messages.error(request,"sorry try again!!")
    else:
        context=Customer_form()
    return render(request, 'harsh/details.html',{'context':context})

def mobile(request,data=None):
    if request.user.is_authenticated:
        try:
            fname=Customer.objects.get(customer=request.user)
            name=fname.Full_name
        except Customer.DoesNotExist:
            name='guest'
    else:
        name='guest'
    if data==None:
        mobiles=Product.objects.filter(category='mobile')
    else:
        mobiles=Product.objects.filter(category='mobile').filter(brand=data)
    return render(request, 'harsh/mobile.html',{'mobile':mobiles,'name':name})
def laptops(request):
    laptop=Product.objects.filter(category='laptop')
    return render(request, 'harsh/laptop.html',{'laptop':laptop})
def add_to_cart(request, id):
    c_user=get_object_or_404(Customer, customer=request.user)
    c_product=get_object_or_404(Product, pk=id)
    object1, status=Cart.objects.get_or_create(user=c_user, product=c_product)
    if not status:
        object1.quantity+=1
        object1.save()
    else:
        object1.save()
    return redirect('cart')
def cart(request):
    customer_instance=get_object_or_404(Customer, customer=request.user)
    context=Cart.objects.filter(user=customer_instance)
    if not context.exists():  # Check if the cart is empty
        messages.warning(request, "Your cart is empty! Redirecting to the homepage.")
        return redirect('home') 
    discountedprice=0
    sellingprice=0
    for i in context:
        discountedprice+=i.product.discounted_price*(i.quantity)
        sellingprice+=i.product.selling_price*(i.quantity)
    total=discountedprice+20
    return render(request, 'harsh/cart.html',{'context':context, 'sp':sellingprice, 'dp':discountedprice,'t':total})
def remove_from_cart(request, id):
    c_user=get_object_or_404(Customer, customer=request.user)
    c_prooduct=get_object_or_404(Cart, user=c_user, product__id=id)
    c_prooduct.delete()
    return redirect('cart')
    
def update_quant(request, id):
    if request.method=='POST':
        product_quant=request.POST.get('quant')
        new_quant=int(product_quant)
        product_instance=get_object_or_404(Cart, product__id=id)
        product_instance.quantity=new_quant
        product_instance.save()
        messages.success(request, "update successfully")
    return redirect('cart')

def check(request):
    c_user=get_object_or_404(Customer, customer=request.user)
    cart_instance=Cart.objects.filter(user=c_user)
    selling_price1=0
    discounte_price1=0
    for i in cart_instance:
        selling_price1+=i.product.selling_price*(i.quantity)
        discounte_price1+=i.product.discounted_price*(i.quantity)
    total=discounte_price1+20
    Fullname=c_user.Full_name
    city=c_user.city
    state=c_user.state
    mobile=c_user.mobile
    return render(request, 'harsh/checklist.html', {'sp':selling_price1, 'dp':discounte_price1,'t':total,'fn':Fullname, 'c':city, 's':state, 'm':mobile})


def place_order(request):
    c_user=get_object_or_404(Customer, customer=request.user)
    cart_object=Cart.objects.filter(user=c_user)
    for i in cart_object:
        instance=Orders.objects.create(user=c_user, product=i.product)
    cart_object.delete()
    messages.success(request, "Order Placed Successfully")
    return render(request, 'harsh/placed.html')
        