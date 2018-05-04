from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'home_phone', 'work_phone')

    # def display_dogs(self):
    #     """
    #     Creates a string for the Genre. This is required to display genre in Admin.
    #     """
    #     return ', '.join([ dog.name for dog in self.dog.all()])

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'owner')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'user', 'get_user_address')
    list_filter = ('start_time',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

