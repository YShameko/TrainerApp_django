from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainers, name='trainers'),
    path('<trainer_id>', views.specific_trainer, name='specific_trainer'),
    path('<trainer_id>/<service_id>', views.trainers_schedule, name='trainers_schedule'),
    path('<trainer_id>/<service_id>/booking', views.book_a_trainer, name='book_a_trainer'),
]