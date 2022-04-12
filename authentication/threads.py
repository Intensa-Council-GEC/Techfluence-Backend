import threading, random, uuid
from django.conf import settings
from django.core.mail import send_mail


class send_organisers_mail(threading.Thread):
    def __init__(self, email, pw):
        self.email = email
        self.pw = pw
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = "Login Credentials"
            message = f"The login credentails toaccess your account are as following.\n Email : {self.email}\n Password : {self.pw}"
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
            subject = "OTP to change password"
            message = f"OTP to change password is {self.token} \nIts valid only for 5 mins."
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject , message ,email_from ,[self.email])
        except Exception as e:
            print(e)
