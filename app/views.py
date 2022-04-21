from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .threads import *
from .models import *
from .utils import *


@api_view(["POST"])
def contactUsForm(request):
    try:
        ser = ContactUsSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({"message":"Respective Authorities will contact you soon"}, status=status.HTTP_200_OK)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AllSoloEventsView(ListAPIView):
    queryset = SoloEventModel.objects.all()
    serializer_class = SoloEventSerializerSmall
class SingleSoloEventView(RetrieveAPIView):
    queryset = SoloEventModel.objects.all()
    serializer_class = SoloEventDetailSerislizer
    lookup_field = "id"


class AllTeamEventsView(ListAPIView):
    queryset = TeamEventModel.objects.all()
    serializer_class = TeamEventSerializerSmall
class SingleTeamEventView(RetrieveAPIView):
    queryset = TeamEventModel.objects.all()
    serializer_class = TeamEventDetailSerislizer
    lookup_field = "id"


@api_view(["POST"])
def soloEventRegistration(request, event_id):
    try:
        event = SoloEventModel.objects.get(id = event_id)
        if not event:
            return Response({"message":"Invalid Event ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        ser = SoloEventRegistration(data=request.data)
        if ser.is_valid():
            if not CollegeModel.objects.filter(id=ser.data["college"]).first():
                return Response({"message":"Invalid College ID"}, status=status.HTTP_404_NOT_FOUND)
            col = CollegeModel.objects.get(id=ser.data["college"])
            email = ser.data["email"]
            user_obj, _ = ParticipantsModel.objects.get_or_create(
                email = email,
                name = ser.data["name"],
                phone = ser.data["phone"], 
                college = col
            )
            participation, _ = SoloParticipation.objects.get_or_create(participant=user_obj, event=event)
            thread_obj = send_solo_participation_acknowledgement(email, event.title)
            thread_obj.start()
            participation.save()
            return Response({"message":"user added to participants"}, status=status.HTTP_200_OK)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def teamEventRegistration(request, event_id):
    try:
        event = TeamEventModel.objects.get(id = event_id)
        if not event:
            return Response({"message":"Invalid Event ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        ser = TeamEventRegistration(data=request.data)
        if ser.is_valid():
            team_username = ser.data["team_username"]
            if TeamModel.objects.filter(team_username=team_username).exists():
                return Response({"message":"This username is taken. Use some other username"}, status=status.HTTP_409_CONFLICT)
            if not CollegeModel.objects.filter(id=ser.data["college"]).first():
                return Response({"message":"Invalid College ID"}, status=status.HTTP_404_NOT_FOUND)
            col = CollegeModel.objects.get(id=ser.data["college"])
            leader_obj, _ = ParticipantsModel.objects.get_or_create(
                email = ser.data["leader_email"],
                name = ser.data["leader_name"],
                phone = ser.data["leader_phone"], 
                college = col
            )
            leader_obj.save()
            team = TeamModel.objects.create(
                name = ser.data["team_name"],
                team_username = team_username,
                leader = leader_obj
            )
            for i in range(1, event.team_size):
                participant_obj, _ = ParticipantsModel.objects.get_or_create(
                    email = ser.data[f"memer_{i}_email"],
                    name = ser.data[f"memer_{i}_name"],
                    phone = ser.data[f"memer_{i}_phone"], 
                    college = col
                )
                team.members.add(participant_obj)
                participant_obj.save()
            team.save()
            participation, _ = TeamParticipation.objects.get_or_create(team=team, event=event)
            email_list = list(team.members.all().values_list("email", flat=True))
            email_list.append(str(team.leader.email))
            thread_obj = send_team_participation_acknowledgement(email_list, event.title)
            thread_obj.start()
            participation.save()
            return Response({"message":"Team added to participants"}, status=status.HTTP_200_OK)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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




# # class EditEventDetails(RetrieveUpdateAPIView):
# #     authentication_classes = [JWTAuthentication]
# #     permission_classes = [IsAuthenticated]
# #     queryset = EventModel.objects.all()
# #     serializer_class = EventDetailSerislizer
# #     lookup_field = "id"
