from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import BooleanField
from base.models import *
from authentication.models import *
from .validators import validate_team_size
from .threads import *


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
    class Meta:
        abstract = True


class SoloEventModel(EventModel):
    def __str__(self):
        return self.title


class TeamEventModel(EventModel):
    team_size = models.PositiveSmallIntegerField(validators=[validate_team_size])
    def __str__(self):
        return self.title

    
class SoloEventRulesModel(BaseModel):
    event = models.ForeignKey(SoloEventModel, related_name="solo_event_rules", on_delete=models.CASCADE)
    rule = models.CharField(max_length=150)
    def __str__(self):
        return self.event


class TeamEventRulesModel(BaseModel):
    event = models.ForeignKey(TeamEventModel, related_name="team_event_rules", on_delete=models.CASCADE)
    rule = models.CharField(max_length=150)
    def __str__(self):
        return self.event


class SoloParticipation(BaseModel):
    participant = models.ForeignKey(ParticipantsModel, related_name="event_participant", on_delete=models.CASCADE)
    event = models.ForeignKey(SoloEventModel, related_name="solo_event_participant", on_delete=models.CASCADE)


class TeamParticipation(BaseModel):
    team = models.ForeignKey(TeamModel, related_name="event_participant_team", on_delete=models.CASCADE)
    event = models.ForeignKey(TeamEventModel, related_name="team_event_participant", on_delete=models.CASCADE)


class SoloWinnerModel(BaseModel):
    event = models.OneToOneField(SoloEventModel, on_delete=models.CASCADE)
    first = models.ForeignKey(ParticipantsModel, related_name="solo_first_place", on_delete=models.CASCADE)
    second = models.ForeignKey(ParticipantsModel, related_name="solo_second_place", on_delete=models.CASCADE)
    def __str__(self):
        return self.event


class TeamWinnerModel(BaseModel):
    event = models.OneToOneField(TeamEventModel, on_delete=models.CASCADE)
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
