"""
URL configuration for emotion_prediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from setup import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home', views.homeprivate, name='privhome'),

    path('register', views.register, name='register'),
    # path('registerr', views.register_error, name='registerr'),
    # path('registersuccess', views.register_success, name='registersuccess'),
    


    path('login', views.user_login, name='login'),
    path('loginerror', views.user_login_error, name='loginerror'),
    path("logout", views.user_logout, name="logout"),


    path('per-paragraph', views.paragraph, name='paragraph'),
    path('per-whole', views.whole, name='whole'),
    path('change', views.change, name='change'),
    path('profile', views.profile, name='profile'),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
    
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('result/download', views.download_result, name="download-result"),
    
    
    
]
    
    
    
    
    
  
    

