from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainers, name='trainers'),
    path('<trainer_id>', views.trainer_page, name='specific_trainer'),
    path('category/<catogory_id>', views.trainers_by_category, name='trainers_by_category'),
    path('<trainer_id>/<service_id>', views.trainer_service_page, name='service_page'),
    path('<trainer_id>/<service_id>/booking', views.book_a_trainer, name='book_a_trainer'),


]