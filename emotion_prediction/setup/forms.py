from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import Users, Emotion, Story, AnalyzedStory

class Userform(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = Users
        fields = ['email', 'last_name', 'first_name', 'username', 'password', 'confirm_password']
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password does not match!")
        return confirm_password
    
    def save(self, commit=True):
        users = super().save(commit=False)

        user = get_user_model().objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], last_name=self.cleaned_data['last_name'], first_name=self.cleaned_data['first_name'], password=self.cleaned_data['password'])
        user.save()
        users.account = user
        if commit:
            users.save()
        return users

