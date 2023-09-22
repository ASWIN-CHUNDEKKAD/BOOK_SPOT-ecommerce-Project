from django.contrib.auth.forms import UserCreationForm

from . models import User,Profile
from django import forms

class CustomUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control my-2','placeholder':'Enter email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2','placeholder':'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-2','placeholder':'Confirm Password'}))
    
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
        
# class Userform(User):
#     class Meta:
#         model = User
#         fields = ('first_name','last_name')
        
# class Profileform(Profile):
#     class Meta:
#         model = Profile
#         fields = ('phone','address','city','state','country','pincode')
        