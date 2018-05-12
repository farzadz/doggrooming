from django.core.mail import send_mail


def send_reminder_email(booking_time, dog_name, user_email):
    print('yo')
    send_mail('Reminder', "This is a reminder from Dog Lovers! to notify about your tomorrow's appointment for %s at %s.".format(dog_name, booking_time),
              'Tom@doglovers.com', [user_email,])