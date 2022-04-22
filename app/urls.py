from django.urls import path
from . import views
from .views import *

urlpatterns = [

	path('contact-us/', views.contactUsForm, name="contact-us"),

	path('all-solo-events/', views.AllSoloEventsView.as_view(), name="all-solo-events"),
	path('solo-event/<id>/', views.SingleSoloEventView.as_view(), name="solo-event"),

	path('all-team-events/', views.AllTeamEventsView.as_view(), name="all-team-events"),
	path('team-event/<id>/', views.SingleTeamEventView.as_view(), name="team-event"),

	path('solo-event-register/<event_id>/', views.soloEventRegistration, name="register-for-solo-event"),
	path('team-event-register/<event_id>/', views.teamEventRegistration, name="register-for-team-event"),
	
	path('notify-participants/', views.sendMailToParticipants, name="send-mail-to-participants"),

	path('participant-list/', views.getEventParticipantsList, name="participant-list"),

	path('participant-list-download/', views.downloadParticipantsList, name="event-participant-list-download"),
	
	path('set-winners/', views.setWinners, name="set-winners"),
	
	# path('generate-certicficated/', views.generateCertificates, name="generate-certicficated"),
	# path('send-certificated/', views.sendCertificates, name="send-certificated"),

	path('notify-all-participants/', views.notifyAllParticipants, name="notify-all-participants"),

]