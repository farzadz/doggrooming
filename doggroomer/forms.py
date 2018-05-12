from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Form

from .models import Dog, Option, Appointment


class SignUpForm(UserCreationForm):
    user_name = forms.CharField(max_length=30, required=True, help_text='Your username')
    # full_name = forms.CharField(max_length=50, required=True, help_text='Your full name')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone = forms.IntegerField(required=True)
    # work_phone = forms.IntegerField(required=False)
    address = forms.CharField(max_length=200, required=True, help_text='Your address')
    postcode = forms.IntegerField(required=True)
    class Meta:
        model = User
        fields = ('user_name', 'email', 'password','address')


class AddDogForm(ModelForm):
    name = forms.CharField(max_length=50, required=True, help_text="What's the name of the fluffy?")
    breed = forms.CharField(max_length=50, required=True)
    birth_date = forms.DateField(required=True)
    class Meta:
        model = Dog
        fields = ('name', 'breed', 'birth_date')


class AddAppointmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ModelForm, self).__init__(*args, **kwargs)
        options = Option.objects.all()
        dogs = Dog.objects.filter(owner=self.request.user)
        for option in options:
            self.fields[option.name] = forms.BooleanField()


        self.fields['DOG'] = forms.ChoiceField(choices=enumerate([dog.name for dog in dogs]), widget=forms.RadioSelect())

    class Meta:
        model = Appointment
        fields = ('description', 'option', 'start_time', 'dog')