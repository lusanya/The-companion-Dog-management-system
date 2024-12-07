from pyexpat.errors import messages
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import Dog, Cart, Order


# Create your views here.

def home(request):
    return render(request,'home.html')# returns the home page

def login_page(request):
    #checking for the request method of the form submission
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        #check for user availability in the system
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Username doesnt exist! ')
            return redirect('/')
        #authenticate the user using the password
        user=authenticate(username=username, password=password)

        if user is None:
            #display error messages if credentials doesnt match
            messages.error(request,'Invalid password ')
            return redirect('/')
        else:
            login(request,user)
            # messages.success(request,'You are now logged in')
            return redirect('/home/')
    return render(request,'login.html')

def register_page(request):
        if request.method=="POST":
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')

            if User.objects.filter(username=username).exists():
                messages.info(request, 'username is already taken')
                return redirect('/register/')

            user=User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email)


            messages.info(request, f"Hello {username} account created successfully! Log in here")
            return redirect('/')

        return render(request,'register.html')

def logout_page(request):
    logout(request)
    messages.success(request, f"You have been logged out. Log in here!")
    return redirect('/')


import random


def password_reset(request):

    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email address not found.")
            return render(request, 'password_reset.html')

        # Generate a 6-digit code for password reset
        reset_code = random.randint(100000, 999999)

        # Send the email with the reset code
        subject = "Password Reset Code"
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_code': reset_code,
        })
        send_mail(subject, message, 'companiondogmanagement@gmail.com', [email], html_message=message)

        # Store the reset code in the session (this is temporary for simplicity)
        request.session['reset_code'] = reset_code
        request.session['user_id'] = user.pk

        messages.success(request, "Password reset code sent! Check your email.")
        return redirect('password_reset_confirm')

    return render(request, 'password_reset.html')

def password_reset_confirm(request):
    """
    Handles the reset of the password using the reset code sent via email.
    """
    # Check if the code is in the session
    if 'reset_code' not in request.session or 'user_id' not in request.session:
        messages.error(request, "Session expired or invalid.")
        return redirect('password_reset')

    # Handle the password reset
    if request.method == "POST":
        entered_code = request.POST.get('code')
        new_password = request.POST.get('password')

        # Check if the entered code matches the one in the session
        if entered_code != str(request.session['reset_code']):
            messages.error(request, "Invalid reset code.")
            return render(request, 'password_reset_confirm.html')

        # Check if the new password is provided
        if new_password:
            user = User.objects.get(pk=request.session['user_id'])
            user.set_password(new_password)
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            # Clear session after reset
            del request.session['reset_code']
            del request.session['user_id']
            return redirect('login')

    # Render reset form (minimalistic)
    return render(request, 'password_reset_confirm.html')



#Dog profiles section
def dog_profiles(request):
    dogs=Dog.objects.all()
    return render(request, 'dog_profiles.html',{'dogs':dogs})

#Adding dog profiles by admin only
@staff_member_required
def add_dog(request):
    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        image=request.FILES.get('image')
        video_url=request.POST.get('video_url')
        price=request.POST.get('price')

        dog=Dog(name=name,description=description, image=image, videos_url=video_url)
        dog.save()
        return redirect('/dog_profiles')
    return render (request, 'add_dog.html')

#Adding a dog to CART by User
@login_required
def add_to_cart(request, dog_id):
    dog=Dog.objects.get(id=dog_id)
    cart_items=Cart.objects.create(user=request.user, dog=dog)
    return redirect('cart')

#cart viewing by user
@login_required
def cart(request):
    cart_items=Cart.objects.filter(user=request.user)
    return render(request,'cart.html',{'cart_items':cart_items})

#Placing of order by the user
@login_required
def place_order(request):
    if request.method=='POST':
        order=Order.objects.create(user=request.user)
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            order.dogs.add(item.dog)
            item.delete()
        order.notify_admin()
        return redirect('order_confirmation', order_id=order.id)
    return render(request,'place_order.html')

#order confirmation
@login_required
def order_confirmation(request, order_id):
    order=Order.objects.get(id=order_id)
    return render(request,'order_confirmation.html',{'order':order})

















