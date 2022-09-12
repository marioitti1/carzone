from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authentication of user
        user = auth.authenticate(request, username=username, password=password)
        # print('user=', user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'User already exists')
                # return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email already exists')
                # return redirect('register')
            else:
                user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                # auth.login(request, user)
                # messages.success(request, 'You are now logged in.')
                # return redirect('dashboard')
                user.save()
                messages.success(request, 'You are registered successfully.')
                # return redirect('login')
        else:
            messages.error(request, 'Password is not match')
            # return redirect('register')
        # return redirect('register')
    return render(request, 'accounts/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        # messages.success(request, 'You are successfully logged out')
        # return redirect('home')
    return redirect('home')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def password_reset(request):
    email = request.POST.get('email', '')
    print('email', email)
    if User.objects.filter(email=email).exists():
        if email:
            try:
                send_mail(subject='Reset password', message='Reset your password', from_email='marioitti1@yandex.ru', recipient_list=[email])
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return HttpResponseRedirect('login')
        else:
            # messages.error(request, 'Make sure that you entered email')
            return render(request, 'accounts/password_reset.html')
    else:
        messages.error(request, 'Make sure that you entered valid email')
        return render(request, 'accounts/password_reset.html')