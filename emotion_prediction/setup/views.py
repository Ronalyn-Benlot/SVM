from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import Userform
from django.contrib.auth import authenticate, login as auth_login,views as auth_views

def home(request):
    return render(request, 'index.html')


def register(request):
    form = Userform

    if request.method == "POST":
        form = Userform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration success!")
            return redirect('login')
    else:
        messages.error(request, "Form is not valid")
    
    context = {"form": form}
    return render(request, 'sign_up.html', context)    
    
    # if request.method == 'POST':
    #     first_name = request.POST['first_name']
    #     last_name = request.POST['last_name']
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     confirm_password = request.POST['confirm_password']

    #     # Check if passwords match
    #     if password != confirm_password:
    #         return redirect(register_error)

    #     # Create a new user
    #     my_user = User.objects.create_user(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
        
    #     return redirect(register_success)
  
    # return render(request, 'sign_up.html')


def register_error(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            return redirect(register_error)

        # Create a new user
        my_user = User.objects.create_user(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
        
        return redirect(register_success)
  
    return render(request, 'sign_up_error.html')

def register_success(request):
    return render(request, "success_reg.html")




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(paragraph)
        else:
             return redirect(user_login_error)

    return render(request, 'logiin.html')


def user_login_error(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(paragraph)
        else:
            return redirect(user_login_error)

    return render(request, 'login_error.html')



from django.contrib.auth.forms import PasswordResetForm


































def paragraph(request):
    return render(request, 'emoji.html')

def whole(request):
    return render(request, 'emoji-whole.html')

def profile(request):
    user = request.user  # Replace this with your user retrieval logic

    context = {
        'user': user,
    }
    return render(request, 'profile.html')

def change(request):
   
        

    
    return render(request,'changepass.html')