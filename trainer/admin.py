from django.contrib import admin

# Register your models here.
from trainer.models import TrainerSchedule, TrainerDescription, Service, Category
admin.site.register(TrainerSchedule)
admin.site.register(TrainerDescription)
admin.site.register(Service)
admin.site.register(Category)
