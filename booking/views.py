# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def booking(request, booking_id):
    # подивитись деталі бронювання
    return HttpResponse("Here are details of your booking:")

def accept(request, booking_id):
    # підтвердити бронювання (доступно тільки для тренера)
    return HttpResponse("This booking has been accepted")

def cancel(request, booking_id):
    # відміна бронювання (з видаленням з бази + розіслати повідомлення)
    return HttpResponse("This booking has been cancelled")
