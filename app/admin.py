from django.contrib import admin
from .models import *


admin.site.register(ContactUsModel)

admin.site.register(SoloEventModel)
admin.site.register(TeamEventModel)

admin.site.register(SoloParticipation)
admin.site.register(TeamParticipation)

admin.site.register(SoloWinnerModel)
admin.site.register(TeamWinnerModel)
