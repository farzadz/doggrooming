from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
]

urlpatterns += [
    path('myappointments/', views.my_appointments, name='my-appointments'),
]