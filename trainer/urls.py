from django.urls import path
from . import views

urlpatterns = [
    path('', views.trainers, name='trainers'),
    path('add_schedule/<trainer_id>', views.add_schedule, name='add_schedule_page'),
    path('edit_schedule/<schedule_id>', views.edit_schedule, name='edit_schedule_page'),
    path('<trainer_id>', views.trainer_page, name='specific_trainer'),
    path('category/<category_id>', views.trainers_by_category, name='trainers_by_category'),
    path('<trainer_id>/<service_id>', views.trainer_service_page, name='service_page'),

]