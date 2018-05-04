from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
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
    return render(request, 'my_appointments.html', context={'appointments': Appointment.objects.filter(user=request.user)})