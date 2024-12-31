from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def user_page(request):
    return HttpResponse("This is an user page")

def specific_user(request, user_id):
    return HttpResponse("This is specific user page")

def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("You are now logged in")
        else:
            return render(request, 'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("You are now logged out")
    return HttpResponse("This is logout page. Login first")

def register_page(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        user.save()
        return HttpResponse("A new user:", username, "was successfully created!")
