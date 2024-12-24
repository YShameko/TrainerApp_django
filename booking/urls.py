from django.urls import path
from . import views

urlpatterns = [
    path('<booking_id>', views.booking, name='view_booking'),
    path('<booking_id>/accept', views.accept, name='booking_accept'),
    path('<booking_id>/cancel', views.cancel, name='booking_cancel'),
]