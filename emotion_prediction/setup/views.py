from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'login.html')

def change(request):
    return render(request, 'changepass.html')

def paragraph(request):
    return render(request, 'emoji.html')

def whole(request):
    return render(request, 'emoji-whole.html')

def profile(request):
    return render(request, 'profile.html')