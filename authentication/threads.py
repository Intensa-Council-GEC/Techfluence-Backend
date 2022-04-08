import threading, random, uuid
from django.conf import settings
from django.core.mail import send_mail


class send_verification_email_seller(threading.Thread):
    def __init__(self, email, token):
        self.email = email
        self.token = token
        threading.Thread.__init__(self)
    def run(self):
        try:
            l = settings.BASE_URL + "api/seller-verify/" + str(self.token) + "/"
            subject = "Link to verify the your Account"
            message = f"The link to verify your email is {l}"
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject , message ,email_from ,[self.email])
        except Exception as e:
            print(e)

class send_forgot_email(threading.Thread):
    def __init__(self, email, token):
        self.email = email
        self.token = token
        threading.Thread.__init__(self)
    def run(self):
        try:
            l = settings.BASE_URL + "api/seller-reset/" + str(self.token) + "/"
            subject = "Link to change password"
            message = f"The link to change your account password {l} \nIts valid only for 5 mins."
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject , message ,email_from ,[self.email])
        except Exception as e:
            print(e)
