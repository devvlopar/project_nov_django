from django.shortcuts import render
from .models import Buyer
from django.core.mail import send_mail
import random
from django.conf import settings
# Create your views here.

def index(request):
    
    return render(request, 'index.html')
    

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
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'message': 'Wrong Password!!'})
        except:
            return render(request, 'login.html', {'message': 'User with this Email does not exist.'})

        
    