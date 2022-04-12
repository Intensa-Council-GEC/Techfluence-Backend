# from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import *
# from .threads import *
# from .models import *
# from .utils import *


# @api_view(["POST"])
# def contactUsForm(request):
#     try:
#         ser = ContactUsSerializer(data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response({"message":"Respective Authorities will contact you soon"}, status=status.HTTP_200_OK)
#         return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # class AllEventsView(ListAPIView):
# #     queryset = EventModel.objects.all()
# #     serializer_class = EventSerializerSmall


# # class SingleEventView(RetrieveAPIView):
# #     queryset = EventModel.objects.all()
# #     serializer_class = EventDetailSerislizer
# #     lookup_field = "id"


# @api_view(["POST"])
# def sendMailToParticipants(request):
#     try:
#         authentication_classes = [JWTAuthentication]
#         permission_classes = [IsAuthenticated]
#         ser = SpecialEmailSerializer(data=request.data)
#         org = OrganisersModel.objects.get(email=request.user.email)
#         if not org:
#             return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
#         event = EventModel.objects.filter(organiser=org)
#         if not event:
#             return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
#         recievers_list = list(EventModel.objects.filter(organiser=True).values_list("email", flat=True))
#         if ser.is_valid():
#             return Response({"message":"All Participants notifed"}, status=status.HTTP_200_OK)
#         return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
# @api_view(["POST"])
# def participantsList(request):
#     try:
#         return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def generateCertificates(request):
#     try:
#         return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def sendCertificates(request):
#     try:
        
#         return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def soloRegistration(request, event_id):
#     try:
#         event = EventModel.objects.get(id = event_id)
#         if not event:
#             return Response({"message":"Invalid Event ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         if event.is_team_even == True:
#             return Response({"message":"This is a team event. Solo Participation Not Allowed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         ser = SoloEventRegistration(data=request.data)
#         if ser.is_valid():
#             name = ser.data["name"]
#             email = ser.data["email"]
#             phone = ser.data["name"]
#             participant = ParticipantsModel.objects.get_or_create()
#         return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def teamRegistration(request, event_id):
#     try:
#         event = EventModel.objects.get(id = event_id)
#         if not event:
#             return Response({"message":"Invalid Event ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         if event.is_team_even == True:
#             return Response({"message":"This is a team event. Solo Participation Not Allowed"}, status=status.HTTP_406_NOT_ACCEPTABLE)
#         ser = TeamEventRegistration(data=request.data)
#         return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# # class EditEventDetails(RetrieveUpdateAPIView):
# #     authentication_classes = [JWTAuthentication]
# #     permission_classes = [IsAuthenticated]
# #     queryset = EventModel.objects.all()
# #     serializer_class = EventDetailSerislizer
# #     lookup_field = "id"
