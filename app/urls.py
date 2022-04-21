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
	
	path('solo-event-participants-notify/', views.soloSendMailToParticipants, name="send-mail-to-participants"),
	path('team-event-participants-notify/', views.teamSendMailToParticipants, name="send-mail-to-participants"),

	path('solo-participant-list/', views.GetSoloEventParticipantsList, name="solo-participant-list"),
	path('team-participant-list/', views.GetTeamEventParticipantsList, name="team-participant-list"),

	# path('solo-event-participant-list-download/', views.participantsList, name="solo-event-participant-list-download"),
	# path('team-event-participant-list-download/', views.participantsList, name="team-event-participant-list-download"),
	
	# path('generate-certicficated/', views.generateCertificates, name="generate-certicficated"),
	# path('send-certificated/', views.sendCertificates, name="send-certificated"),

	# path('set-solo-event-winners/', views.setSoloWinners, name="set-solo-event-winners"),
	# path('set-team-event-winners/', views.setTeamWinners, name="set-team-event-winners"),

	# path('edit-event-details/', views.EditEventDetails.as_view(), name="edit-event-details"),

]