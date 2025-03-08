# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from booking.forms import BookingForm
from booking.models import Booking

@login_required(login_url='/login')
def booking(request, booking_id):
    # подивитись деталі бронювання
    if request.method == 'GET':
        the_booking = Booking.objects.get(pk=booking_id)
        booking_form = BookingForm(instance=the_booking)
        return render(request, 'booking_details.html', {'form': booking_form})
    else: pass

@login_required(login_url='/login/')
def accept(request, booking_id):
    # підтвердити бронювання (доступно тільки для тренера)
    if request.method == 'GET':
        the_booking = Booking.objects.filter(id=booking_id, trainer=request.user).first()
        if the_booking:
            booking_form = BookingForm(instance=the_booking)
            return render(request,'booking_accept.html', {'form': booking_form})
        else: return render(request,'msg_board.html',{'msg':"You have nothing to confirm."})
    else:
        the_booking = Booking.objects.get(id=booking_id)
        the_booking.status = True
        the_booking.save()
        msg = "The booking has been confirmed."
        return render(request, 'msg_board.html', {'msg':msg})

@login_required(login_url='/login/')
def cancel(request, booking_id):
    # відміна бронювання (з видаленням з бази + розіслати повідомлення)
    if request.method == 'GET':
        the_booking = Booking.objects.get(pk=booking_id)
        booking_form = BookingForm(instance=the_booking)
        return render(request,'booking_cancel.html', {'form': booking_form})

    else:
        the_booking = Booking.objects.get(id=booking_id)
        user = the_booking.user.username
        user_mail = the_booking.user.email
        trainer = the_booking.trainer.username
        trainer_mail = the_booking.trainer.email
        the_booking.delete()
        msg = "The booking has been cancelled.<br><br>"
        msg += "The notices will be sent shortly to: <br>"
        msg += user_mail + " (user: " + user + ") and<br>" + trainer_mail + " (trainer: " + trainer + ")<br>"
        return render(request,'msg_board.html', {'msg':msg})
