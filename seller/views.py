from django.shortcuts import render, redirect
from . models import Seller, Product
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def seller_index(request):
    try:
        seller_object = Seller.objects.get(email = request.session['email'])
        return render(request, 'seller_index.html',{'user_object': seller_object})
    except:
        return render(request, 'seller_login.html')


def register(request):
    if request.method == "GET":
        return render(request, 'seller_register.html')
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['re_password']:
            try:
                user_email = Seller.objects.get(email = request.POST['email'] )
                return render(request, 'seller_register.html', {'message': 'Email already exists!!'})
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
                return render(request, 'seller_otp.html', {'message': 'check your MailBox!!!'})
        else:
            return render(request, 'seller_register.html', {'message': 'Both passwords are not same'})

    
def otp(request):
    if request.method == 'POST':
        if generated_otp == int(request.POST['otp']):
            Seller.objects.create(
                first_name = user_dict['first_name'],
                last_name = user_dict['last_name'],
                email = user_dict['email'],
                mobile = user_dict['mobile'],
                password = user_dict['password']
            )
            return render(request, 'seller_login.html', {'message': 'Account created successfully!!'})
        else:
            return render(request, 'seller_otp.html', {'message': 'OTP Does not Match!!'})
    else:
        return render(request, 'seller_login.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'seller_login.html')
    else:
        try:
            session_user = Seller.objects.get(email = request.POST['email'])
            if request.POST['password'] == session_user.password:
                request.session['email'] = session_user.email
                return redirect('seller_index')
            else:
                return render(request, 'seller_login.html', {'message': 'Wrong Password!!'})
        except:
            return render(request, 'seller_login.html', {'message': 'User with this Email does not exist.'})


def logout(request):
    try:
        request.session['email']
        del request.session['email']
        return render(request, 'seller_login.html')
    except:
        return render(request, 'seller_login.html')
        
    

def add_product(request):
    if request.method == 'GET':
        seller_object = Seller.objects.get(email= request.session['email'])
        return render(request, 'add_product.html',{'user_object': seller_object})
    else:
        seller_object = Seller.objects.get(email= request.session['email'])
        Product.objects.create(
            name = request.POST['name'],
            des = request.POST['des'],
            price = request.POST['price'],
            quantity = request.POST['quantity'],
            pic = request.FILES['pic']
        )
        return render(request, 'add_product.html', {'message': 'successfully added!!', 'user_object': seller_object})


def edit_seller_profile(request):
    if request.method == 'GET':
        try:
            seller_object = Seller.objects.get(email = request.session['email'])
            return render(request, 'edit_seller_profile.html', {'user_object': seller_object})
        except:
            return render(request, 'seller_login.html')
    else:
        seller_object = Seller.objects.get(email = request.session['email'])
        seller_object.first_name = request.POST['first_name']
        seller_object.last_name = request.POST['last_name']
        seller_object.mobile = request.POST['mobile']
        seller_object.address = request.POST['address']
        seller_object.dob = request.POST['dob']
        seller_object.gender = request.POST['gender']
        if request.FILES:
            seller_object.pic = request.FILES['pic']
        seller_object.save()
        return render(request, 'edit_seller_profile.html',{'user_object': seller_object})



