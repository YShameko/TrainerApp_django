from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def trainers(request):
    return HttpResponse("All our trainers... You can see them just maybe a bit later")

def specific_trainer(request, trainer_id):
    return HttpResponse("Here will be info about specific trainer and his/her services")

def trainers_schedule(request, trainer_id, service_id):
    return HttpResponse("Here you will be able to see a schedule of the specific trainer (but later)")

def book_a_trainer(request, trainer_id, service_id, booking):
    return HttpResponse("Here you will be able to book a specific trainer (but later)")
