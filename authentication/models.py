from django.db import models
from base.models import *
from .validators import *


class OrganisersModel(BaseUser):
    photo = models.ImageField(upload_to="organiser", height_field=None, width_field=None, max_length=None, null=True)
    token = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.name


class CollegeModel(BaseModel):
    short_form = models.CharField(max_length=50)
    complete_name = models.CharField(max_length=50)
    def __str__(self):
        return self.short_form


class AddOrganiserModel(BaseModel):
    file = models.FileField(upload_to="organiser_excel", max_length=100)


class ParticipantsModel(BaseUser):
    college = models.ForeignKey(CollegeModel, related_name="student_college", on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class TeamModel(BaseModel):
    name = models.CharField(max_length=50)
    team_username = models.CharField(max_length=50, unique=True)
    leader = models.ForeignKey(ParticipantsModel, related_name="team_leader", on_delete=models.CASCADE)
    members = models.ManyToManyField(ParticipantsModel)
    def __str__(self):
        return self.name
    
