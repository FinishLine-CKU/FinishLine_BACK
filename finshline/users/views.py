from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from .models import User
# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            print("인증성공")
            login(request, user)
        else:
            print("인증실패")
    return render(request,"users/login.html")

def logout_view(request):
    logout(request)
    return redirect("user:login")

def signup_view(request):

    if request.method == "POST":
        print(request.POST)
        username=request.POST["username"]
        password=request.POST["password"]
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        email=request.POST["email"]
        student_id=request.POST["student_id"]

        User.objects.create(username,email,password)
        User.last_name=lastname
        User.first_name=firstname
        User.student_id=student_id
        User.save()


        return redirect("user:login")
    
    return render(request,"users/signup.html")