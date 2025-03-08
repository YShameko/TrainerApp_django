from datetime import timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.http import HttpResponse

import trainer.models
import booking.models as booking_models
from trainer.forms import ScheduleForm
from trainer.utils import booking_time_explore
from dateutil import parser
from users import forms

# Create your views here.
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
            return render(request,'msg_board.html', {'msg':greeting_msg})
        else:
            return HttpResponse(register_form.errors)

def trainers_by_category(request, category_id):
    trainers = trainer.models.Service.objects.filter(category=category_id).all()
    category = trainers[0].category.name
    return render(request, 'category.html', {'trainers':trainers, 'category':category})

def trainer_page(request, trainer_id):
    if request.method == "GET":
        service_categories = trainer.models.Category.objects.all()
        my_services = trainer.models.Service.objects.filter(trainer_id=trainer_id).all()
        about_trainer = trainer.models.TrainerDescription.objects.filter(trainer_id=trainer_id).first()
        return render(request, 'trainer.html', {'categories': service_categories,
                                                'services': my_services, 'about_trainer':about_trainer})

@login_required(login_url='/login/')
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
        message += "Please wait until <i>" + current_trainer.first_name + " " + current_trainer.last_name + "</i> confirm your booking.<br><br>"
        message += "You will get the confirmation soon. <br><br>"
        message += "Back to <a href='/user/'>my profile</a>"
        return render(request,'msg_board.html',{'msg':message})

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

@login_required(login_url='/login/')
def service_add(request, trainer_id):
    if request.method == 'POST':
        new_service = trainer.models.Service()
        new_service.price = request.POST.get('price')
        new_service.level = request.POST.get('level')
        new_service.duration = request.POST.get('duration')
        new_service.trainer = User.objects.get(pk=trainer_id)
        category_id = request.POST.get('category')
        new_service.category = trainer.models.Category.objects.get(pk=category_id)
        new_service.save()
        return redirect("/user/")

@login_required(login_url='/login/')
def service_delete(request, service_id):
    if request.method == 'GET':
        the_service = trainer.models.Service.objects.filter(id=service_id).first().delete()
        return redirect("/user/")
    else:
        pass

@login_required(login_url='/login/')
def category_add(request):
    if request.method == 'POST':
        new_category = trainer.models.Category()
        new_category.name = request.POST.get('new_category')
        new_category.save()
        return redirect("/user/")

@login_required(login_url='/login/')
def add_schedule(request, trainer_id):
    if request.method == "GET":
        schedule_form = ScheduleForm(initial={'datetime_start': datetime.today(), 'datetime_end': datetime.today()})
        return render(request, 'trainer_schedule.html', {'trainer':trainer_id,
                                                             'form': schedule_form, 'mode': 'add'})
    else:
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid():
            new_schedule = trainer.models.TrainerSchedule()
            new_schedule.datetime_start = schedule_form.cleaned_data['datetime_start']
            new_schedule.datetime_end = schedule_form.cleaned_data['datetime_end']
            new_schedule.trainer = User.objects.get(pk=request.POST['trainer'])
            new_schedule.save()
            return redirect("/user/")

@login_required(login_url='/login/')
def edit_schedule(request, schedule_id):
    if request.method == "GET":
        the_schedule = trainer.models.TrainerSchedule.objects.get(pk=schedule_id)
        schedule_form = ScheduleForm(initial={'datetime_start': the_schedule.datetime_start,
                                              'datetime_end': the_schedule.datetime_end})
        return render(request, 'trainer_schedule.html', {'schedule':schedule_id,
                                                             'form': schedule_form, 'mode': 'edit'})
    else:
        schedule_form = ScheduleForm(request.POST)
        if schedule_form.is_valid():
            trainer.models.TrainerSchedule.objects.filter(id=request.POST['schedule']).update(**schedule_form.cleaned_data)
            return redirect("/user/")