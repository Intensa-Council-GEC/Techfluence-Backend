from django.urls import path
from . import views
from .views import *

urlpatterns = [

	path('add-organisers/', views.addOrganisers, name="add-organisers"),
	path('organisers-login/', views.organiser_login, name="organisers-login"),
	path('organisers-forgot/', views.organiser_forgot, name="organisers-forgot"),
	path('organisers-reset/', views.organiser_reset, name="organisers-login"),

]