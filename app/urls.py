from django.urls import path
from . import views
from .views import *

urlpatterns = [

	# path('contact-us/', views.contactUsForm, name="contact-us"),

	# path('all-events/', views.AllEventsView.as_view(), name="all-events"),
	# path('event/<id>/', views.SingleEventView.as_view(), name="event"),
	
	# path('send-mail-to-participants/', views.sendMailToParticipants, name="send-mail-to-participants"),
	
	# path('participant-list/', views.participantsList, name="participant-list"),
	
	# path('generate-certicficated/', views.generateCertificates, name="generate-certicficated"),
	# path('send-certificated/', views.sendCertificates, name="send-certificated"),

	# path('solo-register/<event_id>/', views.soloRegistration, name="register-for-solo-event"),
	# path('team-register/<event_id>/', views.teamRegistration, name="register-for-team-event"),
	
	# path('edit-event-details/', views.EditEventDetails.as_view(), name="edit-event-details"),

]