from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def user_page(request):
    return HttpResponse("This is an user page")

def specific_user(request, user_id):
    return HttpResponse("This is specific user page")

def login_page(request):
    return HttpResponse("This is login page")

def logout_page(request):
    return HttpResponse("This is logout page")

def register_page(request):
    return HttpResponse("This is register page")
