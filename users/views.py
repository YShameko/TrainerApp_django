from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect

from trainer.models import Category, Service, TrainerSchedule
from users import forms
from users.models import Rating
from booking import models

# Create your views here.
def main_page(request):
    return render(request, 'index.html')

@login_required(login_url='/login')
def user_page(request):
    if request.method == 'GET':
        user_group = request.user.groups.first().name
        if user_group == 'client':
            bookings = models.Booking.objects.filter(user=request.user).order_by('datetime_start').all()
        else:
            bookings = models.Booking.objects.filter(trainer=request.user).order_by('datetime_start').all()
        my_services = Service.objects.filter(trainer=request.user).all()
        categories = Category.objects.all()
        schedules = TrainerSchedule.objects.filter(trainer=request.user).all()
        update_form = forms.UpdateProfileForm(initial={'first_name': request.user.first_name,
                                                       'last_name': request.user.last_name, 'email': request.user.email})
        return render(request, "profile.html", {'update_form': update_form,
                                            'username': request.user.username, 'user_group': user_group,
                                            'bookings': bookings, 'services': my_services, 'categories': categories,
                                            'schedules': schedules})

    else:
        update_form = forms.UpdateProfileForm(request.POST)
        if update_form.is_valid():
            User.objects.filter(id=request.user.id).update(**update_form.cleaned_data)
            return redirect('/user/')

def specific_user(request, user_id):
    if request.method == 'GET':
        ratings = Rating.objects.filter(recipient=user_id).all()
        user_about = User.objects.get(pk=user_id).username
        return render(request, 'ratings.html', {'ratings': ratings, 'user': user_about})

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
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('/user/')
        else:
            return redirect('/login/', messages.error(request, 'Invalid username or password.'))

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        msg = "You are logged out now. <br>Go to the <a href='/'>main page</a> ?"
        return render(request,'msg_board.html',{'msg':msg})
    return render(request,'msg_board.html',
        {'msg': "This is <u>logout</u> page and you are currently not logged in. You should log in first."})

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
            return render(request,'msg_board.html', {'msg':message})
        else:
            return HttpResponse(register_form.errors)
