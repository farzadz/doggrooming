from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Form

from .models import Dog, Option


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Your username')
    full_name = forms.CharField(max_length=50, required=True, help_text='Your full name')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    home_phone = forms.IntegerField(required=True)
    work_phone = forms.IntegerField(required=False)
    address = forms.CharField(max_length=200, required=True, help_text='Your address')
    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2','address')


class AddDogForm(ModelForm):
    name = forms.CharField(max_length=50, required=True, help_text="What's the name of the fluffy?")
    breed = forms.CharField(max_length=50, required=True)
    birth_date = forms.DateField(required=True)
    class Meta:
        model = Dog
        fields = ('name', 'breed', 'birth_date')


class AddAppointmentForm(Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(Form, self).__init__(*args, **kwargs)
        options = Option.objects.all()
        dogs = Dog.objects.filter(owner=self.request.user)
        for option in options:
            self.fields[option.name] = forms.BooleanField()


        self.fields['DOG'] = forms.ChoiceField(choices=enumerate([dog.name for dog in dogs]), widget=forms.RadioSelect())

