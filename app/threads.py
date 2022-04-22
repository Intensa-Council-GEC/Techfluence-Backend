import threading, pandas
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

context = {}
# context["site_url"] = settings.FRONTEND_URL


class send_contact_email(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        try:
            html_template = 'email/contact.html'
            html_message = render_to_string(html_template, context)
            subject = 'Thanks for filling up Contact Us form.'
            email_from = settings.EMAIL_HOST_USER
            msg = EmailMessage(subject, html_message, email_from, [self.email, settings.ADMIN_EMAIL])
            msg.content_subtype = 'html'
            msg.send()
        except Exception as e:
            print(e)


class send_special_email(threading.Thread):
    def __init__(self, sub, body, email_list):
        self.sub = sub
        self.body = body
        self.email_list = email_list
        threading.Thread.__init__(self)
    def run(self):
        try:
            subject = self.sub
            message = self.body
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject , message ,email_from ,self.email_list)
        except Exception as e:
            print(e)


class send_solo_participation_acknowledgement(threading.Thread):
    def __init__(self, email, event):
        self.email = email
        self.event = event
        threading.Thread.__init__(self)
    def run(self):
        try:
            html_template = 'email/participation.html'
            context["event"] = str(self.event)
            html_message = render_to_string(html_template, context)
            subject = f'You have evrolled for {self.event} event'
            email_from = settings.EMAIL_HOST_USER
            msg = EmailMessage(subject, html_message, email_from, [self.email])
            msg.content_subtype = 'html'
            msg.send()
        except Exception as e:
            print(e)


class send_team_participation_acknowledgement(threading.Thread):
    def __init__(self, email_list, event):
        self.email_list = email_list
        self.event = event
        threading.Thread.__init__(self)
    def run(self):
        try:
            html_template = 'email/participation.html'
            context["event"] = str(self.event)
            html_message = render_to_string(html_template, context)
            subject = f'You have evrolled for {self.event} event'
            email_from = settings.EMAIL_HOST_USER
            msg = EmailMessage(subject, html_message, email_from, self.email_list)
            msg.content_subtype = 'html'
            msg.send()
        except Exception as e:
            print(e)


class generate_solo_event_participant_list_excel(threading.Thread):
    def __init__(self, obj_list, email):
        self.obj_list = obj_list
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        try:
            data = []
            for obj in self.obj_list:
                l1 = [obj.participant.name, obj.participant.email, obj.participant.phone]
                data.append(l1)
            data = pandas.DataFrame(data, columns=['Name', 'Email ID', 'Phone No.'])
            file_name = "data/participant_list/solo.xlsx"
            data.to_excel(file_name)
            sub = "Participants List"
            body = "Excel sheet containing details of participants has been attached bellow."
            msg = EmailMessage(sub, body, settings.EMAIL_HOST_USER, [self.email])
            msg.content_subtype = "html"
            msg.attach_file(str(file_name))
            msg.send()
        except Exception as e:
            print(e)


class generate_team_event_participant_list_excel(threading.Thread):
    def __init__(self, obj_list, email):
        self.obj_list = obj_list
        self.email = email
        threading.Thread.__init__(self)
    def run(self):
        try:
            data = []
            for obj in self.obj_list:
                li, li2 = [], []
                for i in range(1, len(obj.team.members.all())+1):
                    li.append(f"Member {i} Name")
                    li.append(f"Member {i} Email ID")
                    li.append(f"Member {i} Phone No")
                    li2.append(obj.team.members.all()[i-1].name)
                    li2.append(obj.team.members.all()[i-1].email)
                    li2.append(obj.team.members.all()[i-1].phone)
                li3 = [obj.team.name, obj.team.leader.name, obj.team.leader.email, obj.team.leader.phone]
                li3.extend(li2)
                data.append(li3)
            col = ['Team Name', 'Leader Name', 'Leader Email ID', 'Leader Phone No.']
            col.extend(li)
            data = pandas.DataFrame(data, columns=col)
            file_name = "data/participant_list/team.xlsx"
            data.to_excel(file_name)
            sub = "Participants List"
            body = "Excel sheet containing details of participants has been attached bellow."
            msg = EmailMessage(sub, body, settings.EMAIL_HOST_USER, [self.email])
            msg.content_subtype = "html"
            msg.attach_file(str(file_name))
            msg.send()
        except Exception as e:
            print(e)

