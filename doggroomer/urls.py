from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
]

urlpatterns += [
    path('myappointments/', views.my_appointments, name='my-appointments'),
]


urlpatterns += [
    path('signup/', views.signup, name='signup'),
]


urlpatterns += [
    path('user_details/', views.users_details, name='user_details'),
]

urlpatterns += [
    path('profile/', views.profile, name='profile'),
]