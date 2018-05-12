import pytz
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
import datetime
from doggroomer.emails import send_reminder_email
from .forms import *
from django.shortcuts import render, redirect
from .tasks import send_reminder_email_task

from .models import *
from dateutil import parser

def index(request):
    """
    View function for home page of site.
    """
    return render(request,'index.html', context={'services': Option.objects.all()[:3]})

def services(request):
    return render(request, 'services.html', context={'services': Option.objects.all()})


@login_required
def my_appointments(request):
    return render(request, 'my_appointments.html', context={'appointments': Appointment.objects.filter(user=request.user)
                                                            , 'dogs': Dog.objects.filter(owner=request.user)})

@login_required
def booking(request):
    if request.method == "POST":
        # form = AddAppointmentForm(request.POST)
        # if form.is_valid():
            # send_reminder_email_task.apply_async(eta=datetime.datetime.now() + datetime.timedelta(seconds=10), booking_time="Now", dog_name="Husky", email="farzad.vazir@gmail.com")
        options = request.POST.getlist('service_id')
        options_id = [int(option) for option in options]
        start_time = request.POST.get('start_time').split(':')
        print(request.POST.get('appointment_date'))
        appointment_date = request.POST.get('appointment_date').split('-')
        date = datetime.date(int(appointment_date[0]), int(appointment_date[1]), int(appointment_date[2]))
        time_ = datetime.time(int(start_time[0]), int(start_time[1]))
        print('date is')
        print(date)
        print('time is')
        print(time_)
        final_datetime = datetime.datetime.combine(date, time_)
        print('final')
        print(final_datetime)
        dog = Dog.objects.get(pk=int(request.POST.get('dog_id')))
        description = request.POST.get('comments')
        appointment = Appointment.objects.create(user=request.user,
                                                 description=description, dog=dog, start_time=final_datetime)
        appointment.save()
        for option_id in options_id:
            appointment.option.add(Option.objects.get(pk=option_id))
        appointment.save()
        return render(request, 'profile.html',context={ 'appointments': Appointment.objects.filter(user=request.user),
                                                    'dogs': Dog.objects.filter(owner=request.user)})
    else:
            ########################################
        times = ['9:00', '10:30', '12:00', '13:30']
        return render(request, 'booking2.html', {'services': Option.objects.all(),
                                                'dogs': Dog.objects.filter(owner=request.user),
                                                'form': AddAppointmentForm(request=request),
                                                 'times':times})

def signup(request):
    if request.method == 'POST':
        # form = SignUpForm(request.POST)
        # if form.is_valid():
            user = User.objects.create_user(username=request.POST.get('email'), password=request.POST.get('password'), email=request.POST.get('email'))
            user.save()
            user.refresh_from_db()
            user.profile.address = request.POST.get('address')
            user.profile.full_name = request.POST.get('name')
            user.profile.phone = request.POST.get('phone')
            user.save()
            user = authenticate(username=user.username, password=request.POST.get('password'))
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = AddDogForm(request.POST)
        if form.is_valid():
            # dog = form.save()
            # dog.refresh_from_db()
            dog = Dog(owner=request.user)
            dog.name = form.cleaned_data.get('name')
            dog.breed = form.cleaned_data.get('breed')
            dog.birth_date = form.cleaned_data.get('birth_date')
            dog.save()
            return redirect('profile')
        else:
            return request('profile')
    else:
        form = AddDogForm()

        melbourne_tz = pytz.timezone('Australia/Melbourne')
        melbourne_dt = melbourne_tz.localize(datetime.datetime.now() + datetime.timedelta(seconds=10))
        give_this_to_celery = melbourne_dt.astimezone(pytz.UTC)
        # send_reminder_email_task.apply_async(("Now", "Husky", "farzad.vazir@gmail.com"), eta=give_this_to_celery)

        return render(request, 'profile.html', context={'form': form , 'appointments': Appointment.objects.filter(user=request.user),
                                                    'dogs': Dog.objects.filter(owner=request.user)})
# @login_required
# def book_appointment(request):

@permission_required('is_superuser')
def users_details(request):
    return render(request, 'users_details.html', context={'profiles': Profile.objects.all()})

@login_required
def delete_appointment(request, id):

    app = Appointment.objects.get(pk=id)
    if app:
        app.delete()
    return redirect('profile')
     # return render(request, 'profile.html',context={'appointments': Appointment.objects.filter(user=request.user),
     #                                                'dogs': Dog.objects.filter(owner=request.user)})
@login_required
def delete_dog(request, id):
    dog = Dog.objects.get(pk=id)
    if dog:
        dog.delete()
    return redirect('profile')