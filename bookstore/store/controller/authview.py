from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from store.forms import CustomUserForm
from django.http import HttpResponse


'''user registration'''
def register(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are Logged in")
        return redirect('home')
    else:
        form = CustomUserForm
        if request.method == 'POST':
            form = CustomUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Registered successfully,Login to Continue")
                return redirect('loginpage')
        context = {'form':form}
        return render(request,'store/auth/register.html',context)

'''Login page functionality'''
def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are Logged in")
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            
            user = authenticate(request,username=name,password=passwd)
            
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in successfully')
                return redirect('home')
            else:
                messages.error(request,"Invalid username or Password")
                return redirect('loginpage')
        
        return render(request,'store/auth/login.html')
    
    
'''Logout'''
def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout Successfully")
    return redirect('home')

'''edit profile functionality'''
def edit_profile(request):
    return render(request,'store/auth/edit_profile.html')