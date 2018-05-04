from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.urls import reverse


class Option(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Enter grooming option here")
    price = models.FloatField("Price to be charged")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name + " " + str(self.price)

class Dog(models.Model):

    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    breed = models.CharField(max_length=50)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return str(self.name) + " owner: " + str(self.owner)


# class User(models.Model):
#
#     name = models.CharField(max_length=50, null=False)
#     email = models.EmailField(max_length=60, null=False)
#     home_phone = models.IntegerField(help_text="Enter your phone without preceding zeros.", null=False)
#     work_phone = models.IntegerField(help_text="Enter your phone without preceding zeros.")
#     address = models.CharField(max_length=200)
#     def __str__(self):
#         return self.name

class Appointment(models.Model):

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=1000, help_text='Enter your specific comments here')
    option = models.ManyToManyField(Option, help_text='Select options for this appointment')

    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, null=False)
    start_time = models.DateTimeField(verbose_name="Starting time of the appointment")

    def get_user_address(self):
        return self.user.address

    get_user_address.short_description = 'Address'


    def __str__(self):
        """
        String for representing the Model object.
        """
        return str(self.user) + " " + str(self.start_time)

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this appointment.
        """
        return reverse('appointment-detail', args=[str(self.id)])

