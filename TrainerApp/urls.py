"""
URL configuration for TrainerApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import users.views, trainer.views, booking.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # ------------------- U S E R S --------------------------------------
    path('user/', include('users.urls')),
    path('', users.views.main_page, name='main_page'),
    path('login/', users.views.login_page, name='user_login'),
    path('logout/', users.views.logout_page, name='user_logout'),
    path('register/', users.views.register_page, name='user_register'),
    path('register/trainer/', trainer.views.trainer_register, name='trainer_register'),

    # -------------------  T R A I N E R ---------------------------------
    path('trainer/', include('trainer.urls')),
    path('service/', trainer.views.service_page, name='trainer_service'),
    path('service/add/<trainer_id>', trainer.views.service_add, name='trainer_service_add'),
    path('service/delete/<service_id>', trainer.views.service_delete, name='trainer_service_delete'),
    path('category/add', trainer.views.category_add, name='trainer_category_add'),

    # -------------------  B O O K I N G ---------------------------------
    path('booking/', include('booking.urls')),
]
