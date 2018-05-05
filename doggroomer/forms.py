from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Dog


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