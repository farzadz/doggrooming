from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from .forms import SignUpForm, AddDogForm
from django.shortcuts import render, redirect


from .models import *


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
                                                            , 'dogs': Dog.objects.filter(user=request.user)})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.address = form.cleaned_data.get('address')
            user.profile.full_name = form.cleaned_data.get('full_name')
            user.profile.home_phone = form.cleaned_data.get('home_phone')
            user.profile.work_phone = form.cleaned_data.get('work_phone')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
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
        form = AddDogForm()
        return render(request, 'profile.html', context={'form': form , 'appointments': Appointment.objects.filter(user=request.user),
                                                    'dogs': Dog.objects.filter(owner=request.user)})

@permission_required('is_superuser')
def users_details(request):
    return render(request, 'users_details.html', context={'profiles': Profile.objects.all()})


