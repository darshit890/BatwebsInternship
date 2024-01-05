from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Student
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    std=Student.objects.all()
    return render(request, "std/home.html", {"std":std})

def std_add(request):
    if request.method=="POST":
        print("Added")
        std_roll=request.POST.get("std_roll")
        std_name=request.POST.get("std_name")
        std_email=request.POST.get("std_email")
        std_address=request.POST.get("std_address")
        std_phone=request.POST.get("std_phone")
        
        s=Student()
        s.roll=std_roll
        s.name=std_name
        s.email=std_email
        s.address=std_address
        s.phone=std_phone
        s.save()
        return redirect("/std/home/")
    
    return render(request, "std/add_std.html", {})

def delete_std(request,roll):
    s=Student.objects.get(pk=roll)
    s.delete()
    
    return redirect("/std/home/")

def update_std(request,roll):
    std=Student.objects.get(pk=roll)
    return render(request, "std/update_std.html",{'std':std})

def do_update_std(request,roll):
    std_roll=request.POST.get("std_roll")
    std_name=request.POST.get("std_name")
    std_email=request.POST.get("std_email")
    std_address=request.POST.get("std_address")
    std_phone=request.POST.get("std_phone")
    
    std=Student.objects.get(pk=roll)
    
    std.roll=std_roll
    std.name=std_name
    std.email=std_email
    std.address=std_address
    std.phone=std_phone
    std.save()
    
    return redirect("/std/home/")

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        
        if pass1!=pass2:
            return HttpResponse('Passwords do not match')
        else:
            if User.objects.filter(username=uname).exists():
                # Handle the case where the username is not unique
                # You might want to return an error message to the user or redirect them to a different page
                return HttpResponse('Username is not unique')

            # Continue with user creation if the username is unique
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                print(uname,email,pass1,pass2)
                my_user.save()
                # ... rest of your code
            except IntegrityError as e:
                # Handle IntegrityError, e.g., return an error message to the user or log the error
                return HttpResponse('Error creating user: {}'.format(str(e)))
        
            return redirect("login")
        
    return render(request, 'std/signup.html')

def LoginPage(request):
    if request.method=="POST":
        username=request.POST.get("username")
        pass1=request.POST.get("pass")
        user=authenticate(request, username=username, password=pass1) 
        if user is not None:
            login(request, user)
            return redirect("/std/home")
        else:
            return HttpResponse("Invalid username or password")
        
    return render(request, 'std/login.html')

def LogoutPage(request):
    logout(request)
    return redirect("login")