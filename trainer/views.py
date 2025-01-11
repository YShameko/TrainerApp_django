from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse

import trainer.models


# Create your views here.
def category_page(request):
    pass
def trainers(request):
    all_trainers = trainer.models.Service.objects.all()
    return render(request, 'trainers.html', {'trainers':all_trainers})
def trainer_register(request):
    if request.method == 'GET':
        return render(request, 'register_trainer.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        trainer_group = Group.objects.get(name='trainer')
        user.groups.add(trainer_group)
        user.save()
        return HttpResponse("A new trainer: <b>"+username+"</b> was successfully created!")

def trainer_page(request, trainer_id):
    if request.user.groups.filter(name='trainer').exists():
        if request.method == "GET":
            service_categories = trainer.models.Category.objects.all()
            my_services = trainer.models.Service.objects.filter(trainer_id=trainer_id).all()
            return render(request, 'trainer.html', {'categories': service_categories,
                                                                        'services': my_services})
    else:
        trainer_model = User.objects.get(pk=trainer_id)
        trainer_data = trainer.models.TrainerDescription.objects.filter(trainer=trainer_model)
        trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=trainer_model)
        return render(request, 'account.html', {'trainer_data': trainer_data,
                                                'trainer_schedule': trainer_schedule})

def trainers_schedule(request, trainer_id, service_id):
    return HttpResponse("Here you will be able to see a schedule of the specific trainer (but later)")

def trainer_service_page(request, trainer_id, service_id):
    return HttpResponse("trainer_service_page")

def service_page(request):
    if request.method == "GET":
        services = trainer.models.Service.objects.all()
        return render(request, 'services.html', {'services':services})

    else:
        if request.user.groups.filter(name='trainer').exists():
            form_data = request.POST
            serv_cat = trainer.models.Category.objects.get(pk=form_data['category'])
            service = trainer.models.Service(
                price=form_data['price'],
                category=serv_cat,
                level=form_data['level'],
                duration=form_data['duration'],
                trainer=request.user,
            )
            service.save()
            return redirect("/trainer/")

def book_a_trainer(request, trainer_id, service_id, booking):
    return HttpResponse("Here you will be able to book a specific trainer (but later)")
