from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password=password )
        if user is not None:
            login(request, user)
            return redirect('create_grn')
        else:
            messages.success(request, ("There was an error logging in, Try again"))
            return redirect('login_user')
    else:
        return render(request, 'authenticate/login_user.html', {})
    
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return redirect('login_user')
    return redirect('login_user')
