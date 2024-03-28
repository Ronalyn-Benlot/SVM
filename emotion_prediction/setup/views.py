from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import Userform, StoryForm
from .models import AnalyzedStory
from django.contrib.auth import authenticate, logout, login as auth_login,views as auth_views
from django.contrib.auth.decorators import login_required

# PDF DOWNLAOD
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import get_template
import io
import xhtml2pdf.pisa as pisa
from django.core.paginator import Paginator

def home(request):
    return render(request, 'index.html')

def homeprivate(request):
    return render(request, 'privateindex.html')

def register(request):
    form = Userform
    success = False

    if request.method == "POST":
        form = Userform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration success!")
            success = True
            return redirect('login')
        else:
            messages.error(request, "Form is not valid")
            success = False
    
    else:
        form = Userform()
    
    context = {
        "form": form, 
        "success": success
        }
    
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


# def register_error(request):
#     if request.method == 'POST':
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         # Check if passwords match
#         if password != confirm_password:
#             return redirect(register_error)

#         # Create a new user
#         my_user = User.objects.create_user(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
        
#         return redirect(register_success)
  
#     return render(request, 'sign_up_error.html')

# def register_success(request):
#     return render(request, "success_reg.html")




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


def user_logout(request):
    logout(request)
    return redirect("home")


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

    return render(request, 'logiin_error.html')



# from django.contrib.auth.forms import PasswordResetForm

@login_required(login_url='/login')
def paragraph(request):
    form = StoryForm()
    success = False

    recent_user_story = None  

    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save(request)
            user_stories = AnalyzedStory.objects.filter(user=request.user.users).order_by('-id')
            recent_user_story = user_stories.first()
            success = True

    context = {
        'form': form, 
        'analyzed_story': recent_user_story, 
        "success": success
        }
    
    return render(request, 'emoji.html', context)


@login_required(login_url='/login')
def profile(request):
    logged_user = request.user.users  
    user_stories = AnalyzedStory.objects.filter(user=logged_user).order_by('-id')

    # Paginate the user stories
    paginator = Paginator(user_stories, 7)  
    page_number = request.GET.get('page')
    user_stories_paginated = paginator.get_page(page_number)

    context = {
        'logged_user': logged_user,
        'user_stories': user_stories_paginated
    }
    return render(request, 'profile.html', context)

def change(request):
   
        

    
    return render(request,'changepass.html')

@login_required(login_url='/login')
def whole(request):
    form = StoryForm()
    success = False
    recent_user_story = None
    content = None

    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)

        uploaded_file = request.FILES.get('file')
        
        if uploaded_file:
            file_content = uploaded_file.read().decode('utf-8')
            content = file_content
            form.data = form.data.copy()
            form.data['story'] = file_content # store the decoded story from the uploaded file to story field
            print(content)

        if form.is_valid():
            form.save(request)
            success = True
            user_stories = AnalyzedStory.objects.filter(user=request.user.users).order_by('-id')
            recent_user_story = user_stories.first()
        else:
            print("Form is not valid:", form.errors)

    context = {
        'form': form,
        'analyzed_story': recent_user_story,
        'success': success,
        'content': content, 
    }

    return render(request, 'emoji-whole.html', context)


# download result
def download_result(request):
    logged_user = request.user.users  
    user_stories = AnalyzedStory.objects.filter(user=logged_user).order_by('-id')
    recent_user_story = user_stories.first()

    context = {
        'logged_user': logged_user,
        'user_stories': user_stories,
        'recent_user_story': recent_user_story
    }

    # Download as PDF
    template = get_template('registration/pdf.html')
    html = template.render(context)
    pdf_file = io.BytesIO()
    pisa.CreatePDF(html, dest=pdf_file, orientation='Portrait', pagesize='A4')
    
    # Create and return the PDF response
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="result.pdf"'
    return response