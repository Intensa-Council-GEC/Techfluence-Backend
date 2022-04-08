from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from base.models import *
from .threads import *
from authentication.models import *


class ContactUsModel(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()
    def __str__(self):
        return self.name


class EventModel(BaseModel):
    title = models.CharField(max_length=35)
    short_desc = models.CharField(max_length=150)
    description = models.TextField()
    logo = models.ImageField(upload_to="event", height_field=None, width_field=None, max_length=None)
    organiser = models.ForeignKey(OrganisersModel, on_delete=models.CASCADE)
    entry_fees = models.IntegerField()
    whats_app = models.URLField(max_length=200, null=True, blank=True)
    team_event = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class RulesModel(BaseModel):
    event = models.ForeignKey(EventModel, related_name="event_rules", on_delete=models.CASCADE)
    rule = models.CharField(max_length=150)


class SoloWinnerModel(BaseModel):
    event = models.OneToOneField(EventModel, on_delete=models.CASCADE)
    first = models.ForeignKey(ParticipantsModel, related_name="solo_first_place", on_delete=models.CASCADE)
    second = models.ForeignKey(ParticipantsModel, related_name="solo_second_place", on_delete=models.CASCADE)
    def __str__(self):
        return self.event


class TeamWinnerModel(BaseModel):
    event = models.OneToOneField(EventModel, on_delete=models.CASCADE)
    first = models.ForeignKey(TeamModel, related_name="team_first_place", on_delete=models.CASCADE)
    second = models.ForeignKey(TeamModel, related_name="team_second_place", on_delete=models.CASCADE)
    def __str__(self):
        return self.event

        

@receiver(pre_save, sender=ContactUsModel)
def send_email(sender, instance, *args, **kwargs):
    try:
        thread_obj = send_contact_email(instance.email)
        thread_obj.start()
    except Exception as e:
        print(e)