from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
from django.dispatch import receiver
from django.urls import reverse


class Option(models.Model):

    name = models.CharField(max_length=200, help_text="Enter grooming option here")
    price = models.FloatField("Price to be charged")

    def __str__(self):
        return self.name + " " + str(self.price)


# class Client(AbstractUser):
#     name = models.CharField(max_length=50, blank=False)
#     address = models.TextField(max_length=300, blank=False)
#     home_phone = models.IntegerField(null=False, blank=False)
#     work_phone = models.IntegerField(null=True, blank=True)

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    address = models.CharField(max_length=300, blank=False)
    phone = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return "user: " + str(self.user) + " " + " address:" + self.address

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Appointment(models.Model):

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    description = models.TextField(max_length=1000, help_text='Enter your specific comments here')
    option = models.ManyToManyField(Option, help_text='Select options for this appointment')

    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, null=False)
    start_time = models.DateTimeField(verbose_name="Starting time of the appointment")

    def get_user_address(self):
        return self.user.profile.address

    get_user_address.short_description = 'Address'


    def __str__(self):
        return str(self.user) + " " + str(self.start_time)

    def get_absolute_url(self):
        return reverse('appointment-detail', args=[str(self.id)])


