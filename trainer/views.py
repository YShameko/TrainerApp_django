from datetime import timedelta, datetime, date

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse

import trainer.models
import booking.models as booking_models
from users.views import specific_user
from trainer.utils import booking_time_explore
from dateutil import parser
from users import forms

# Create your views here.
def category_page(request):
    pass
def trainers(request):
    all_trainers = trainer.models.Service.objects.all()
    return render(request, 'trainers.html', {'trainers':all_trainers})
def trainer_register(request):
    if request.method == 'GET':
        register_form = forms.RegisterForm()
        return render(request, 'register_trainer.html', context={'register_form':register_form})
    else:
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            created_trainer = register_form.save()
            trainer_group = Group.objects.get(name='trainer')
            created_trainer.groups.add(trainer_group)
            created_trainer.save()
            greeting_msg = "A new trainer: <b><i>"+register_form.cleaned_data['username']+"</i></b> was successfully created!"
            greeting_msg += "<br><br>Welcome!<br> Now you can <a href='/login'>login</a> into your new account."
            return HttpResponse(greeting_msg)
        else:
            return HttpResponse(register_form.errors)

def trainers_by_category(request, category_id):
    return HttpResponse("Everything is temporary. Even this message.")

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
    current_trainer = User.objects.get(pk=trainer_id)
    specific_service = trainer.models.Service.objects.get(pk=service_id)
    if request.method == 'GET':
        available_times = []
        days_from_today = 1
        today = datetime.today()
        while days_from_today <= 7:
            cur_date = (today + timedelta(days=days_from_today)).date()
            trainer_bookings = booking_models.Booking.objects.filter(trainer=current_trainer,
                                                                    datetime_start__date=cur_date).all()
            trainer_bookings_lst_tpl = [(book.datetime_start, book.datetime_end,) for book in trainer_bookings]
            trainer_schedule = trainer.models.TrainerSchedule.objects.filter(trainer=current_trainer,
                                                                             datetime_start__date=cur_date).first()
            if trainer_schedule:
                trainer_schedule_lst = [trainer_schedule.datetime_start, trainer_schedule.datetime_end]
                available_times += trainer.utils.booking_time_explore(trainer_schedule_lst, trainer_bookings_lst_tpl,
                                                                                            specific_service.duration)
            days_from_today += 1
        return render(request, 'trainer_service_page.html',
                            context={'service':specific_service, 'available_times': available_times})
    else:
        booking_start = parser.parse(request.POST.get('training_start'))
        booking_end = booking_start + timedelta(minutes=specific_service.duration)
        new_booking = booking_models.Booking(trainer=current_trainer, user=request.user, service=specific_service,
                datetime_start=booking_start, datetime_end=booking_end, status=False)
        new_booking.save()
        message = "Your booking at " + request.POST.get('training_start') + " was created successfully!<br>"
        message += "Please wait until <i>" + current_trainer.first_name + " " + current_trainer.last_name + "</i> confirm your booking.<br>>"
        message += "You will get the confirmation soon. <br>"
        return HttpResponse(message)

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
