from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('all-events/', views.AllEventsView.as_view(), name="all-events"),
	path('event/<id>/', views.SingleEventView.as_view(), name="event"),
	
	path('send-mail-to-participants/', views.sendMailToParticipants, name="send-mail-to-participants"),
]