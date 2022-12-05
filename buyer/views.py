from django.core.mail  import send_mail
from django.shortcuts import render, redirect
from .models import Buyer, Cart
from seller.models import Product
from django.core.mail import send_mail
import random
from django.conf import settings
from django.http import HttpResponse
# Create your views here.

def index(request):
    all_products = Product.objects.all()
    try:
        user_object = Buyer.objects.get(email = request.session['email'])
        return render(request, 'index.html', {'user_object': user_object, 'all_products' : all_products})
    except:
        return render(request, 'index.html',{'all_products' : all_products})
    
#DRY : Don't Repeat Yourself

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['re_password']:
            try:
                user_email = Buyer.objects.get(email = request.POST['email'] )
                return render(request, 'register.html', {'message': 'Email already exists!!'})
            except:
                global user_dict
                user_dict = {
                    'first_name' : request.POST['first_name'],
                    'last_name' : request.POST['last_name'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'password' : request.POST['password'],
                }
                subject = 'Registration!!!'
                global generated_otp
                generated_otp = random.randint(100000, 999999)
                message = f'Your OTP is {generated_otp}.'
                from_email = settings.EMAIL_HOST_USER
                list1 = [request.POST['email']]
                send_mail(subject, message, from_email, list1)
                return render(request, 'otp.html', {'message': 'check your MailBox!!!'})
        else:
            return render(request, 'register.html', {'message': 'Both passwords are not same'})

def otp(request):
    if request.method == 'POST':
        if generated_otp == int(request.POST['otp']):
            Buyer.objects.create(
                first_name = user_dict['first_name'],
                last_name = user_dict['last_name'],
                email = user_dict['email'],
                mobile = user_dict['mobile'],
                password = user_dict['password']
            )
            return render(request, 'login.html', {'message': 'Account created successfully!!'})
        else:
            return render(request, 'otp.html', {'message': 'OTP Does not Match!!'})
    else:
        return render(request, 'login.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        try:
            session_user = Buyer.objects.get(email = request.POST['email'])
            if request.POST['password'] == session_user.password:
                request.session['email'] = session_user.email
                return redirect('index')
            else:
                return render(request, 'login.html', {'message': 'Wrong Password!!'})
        except:
            return render(request, 'login.html', {'message': 'User with this Email does not exist.'})

        
def logout(request):
    del request.session['email']
    return redirect('index')

def edit_profile(request):
    user_object = Buyer.objects.get(email = request.session['email'])
    return render(request, 'edit_profile.html', {'user_object': user_object})


def add_to_cart(request, pk):
    try:
        Cart.objects.create(
            product = Product.objects.get(id = pk),
            buyer = Buyer.objects.get(email = request.session['email']),
            quantity = request.GET[str(pk)]
        )
        return redirect('index')
    except KeyError:
        return render(request, 'login.html')
    except:
        return render(request, '500.html')
    

def checkout(request):
    user_object = Buyer.objects.get(email = request.session['email'])
    cart_products = Cart.objects.filter(buyer = user_object)
    return render(request, 'checkout.html',{'user_object': user_object, 'cart_products': cart_products, 'total_items': len(cart_products)})

def make_payment(request):
    user_object = Buyer.objects.get(email = request.session['email'])
    cart_products = Cart.objects.filter(buyer = user_object)
    total_price = 0
    for item in cart_products:
        total_price += item.product.price * item.quantity

    return render(request, 'payment.html', {'cart_products': cart_products , 'total_price' : total_price} )

def drop_cart_product(request, pk):
    del_object = Cart.objects.get(id = pk)
    del_object.delete()
    user_object = Buyer.objects.get(email = request.session['email'])
    cart_products = Cart.objects.filter(buyer = user_object)
    return render(request, 'checkout.html', {'cart_products': cart_products, 'total_items': len(cart_products), 'user_object': user_object})