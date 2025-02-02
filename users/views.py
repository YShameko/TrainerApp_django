from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

import users.forms
from users import forms

# Create your views here.
def user_page(request):
    return HttpResponse("This is an user page")

def specific_user(request, user_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            current_user = User.objects.get(pk=user_id)
            update_form = forms.UpdateProfileForm(initial={'first_name': current_user.first_name,
                                                           'last_name': current_user.last_name, 'email': current_user.email})
            return render(request, "profile.html", {'update_form': update_form,
                                                                'username': current_user.username, 'user_id': user_id})

        else:
            update_form = forms.UpdateProfileForm(request.POST)
            if update_form.is_valid():
                modified_user = User.objects.filter(id=user_id).update(**update_form.cleaned_data)
                msg = "Your profile has been updated! Click here to <a href='/user/"+user_id+"'>go back</a> to your profile."
                msg += "<br>Or you can choose any other page to visit :)"
                return HttpResponse(msg)
    else:
        msg = "You are not logged in. To view this page you need to <a href='/login'>login</a> first."
        return HttpResponse(msg)

def login_page(request):
    if request.method == 'GET':
        login_form = forms.LoginForm()
        return render(request, 'login.html', context={'login_form': login_form})
    else:
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("You are now logged in")
        else:
            return redirect('/login/', messages.error(request, 'Invalid username or password.'))

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("You are logged out now")
    return HttpResponse("This is <u>logout</u> page and you are currently not logged in. You should log in first.")

def register_page(request):
    if request.method == 'GET':
        register_form = forms.RegisterForm()
        return render(request, 'register.html', context={'register_form': register_form})
    else:
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            created_user = register_form.save()
            client_group = Group.objects.get(name='client')
            created_user.groups.add(client_group)
            created_user.save()
            message = "A new user: <b><i>" + register_form.cleaned_data['username'] + "</i></b> was successfully created!"
            message += "<br><br>Welcome!<br> Now you can <a href='/login'>login</a> into your new account."
            return HttpResponse(message)
        else:
            return HttpResponse(register_form.errors)
