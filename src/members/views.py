from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password )
        if user is not None:
            login(request, user)
            return redirect ('create_items')
        else:
            messages.success(request, ("There was an error loggin in, Try again"))
            return redirect('login_user')
    else:
        return render(request, 'authenticate/login_user.html', {})
    
@login_required(login_url="login_user")
def home(request):
    return render(request, 'authenticate/home.html')
# Create your views here.
