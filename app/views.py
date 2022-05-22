from rest_framework.generics import ListAPIView, RetrieveAPIView
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
            res = checkUser(email)
            if res:
                user_obj = ParticipantsModel.objects.get(email=email)
            else:
                user_obj = ParticipantsModel.objects.create(
                    email = email,
                    name = ser.data["name"],
                    phone = ser.data["phone"], 
                    college = col
                )
            participation, _ = SoloParticipation.objects.get_or_create(participant=user_obj, event=event)
            thread_obj = send_solo_participation_acknowledgement(email, event.title)
            thread_obj.start()
            user_obj.save()
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


@api_view(["POST"])
def sendMailToParticipants(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        if not OrganisersModel.objects.filter(email=request.user).first():
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        org = OrganisersModel.objects.get(email=request.user)
        res = checkTeamEvent(org)
        recievers_list = []
        if not res:
            event = SoloEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            participants = SoloParticipation.objects.filter(event=event)
            for i in participants:
                recievers_list.append(i.participant.email)
        else:
            event = TeamEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            teams = TeamParticipation.objects.filter(event=event)
            for i in teams:
                recievers_list.extend(list(i.team.members.all().values_list("email", flat=True)))
                recievers_list.append(i.team.leader.email)
        ser = SpecialEmailSerializer(data=request.data)
        if ser.is_valid():
            thread_obj = send_special_email(ser.data["sub"], ser.data["body"], recievers_list)
            thread_obj.start()
            return Response({"message":"All Participants notifed"}, status=status.HTTP_200_OK)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def getEventParticipantsList(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        if not OrganisersModel.objects.filter(email=request.user).first():
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        org = OrganisersModel.objects.get(email=request.user)
        res = checkTeamEvent(org)
        if not res:
            event = SoloEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            objs = SoloParticipation.objects.filter(event=event)
            ser = SoloEventParticipantsListSerializer(objs, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)
        event = TeamEventModel.objects.get(organiser=org)
        if not event:
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        objs = TeamParticipation.objects.filter(event=event)
        ser = TeamEventParticipantsListSerializer(objs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def downloadParticipantsList(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        if not OrganisersModel.objects.filter(email=request.user).first():
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        org = OrganisersModel.objects.get(email=request.user)
        res = checkTeamEvent(org)
        if not res:
            event = SoloEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            objs = SoloParticipation.objects.filter(event=event)
            thread_obj = generate_solo_event_participant_list_excel(objs, org.email)
            thread_obj.start()
        else:
            event = TeamEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            objs = TeamParticipation.objects.filter(event=event)
            thread_obj = generate_team_event_participant_list_excel(objs, org.email)
            thread_obj.start()
        return Response({"message":"Excel Sheet sent to your mail"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def setWinners(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        if not OrganisersModel.objects.filter(email=request.user).first():
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        org = OrganisersModel.objects.get(email=request.user)
        ser = SetWinnersSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        first_id = ser.data["first"]
        second_id = ser.data["second"]
        res = checkTeamEvent(org)
        if not res:
            event = SoloEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            first_place = ParticipantsModel.objects.get(id=first_id)
            second_place = ParticipantsModel.objects.get(id=second_id)
            if not (SoloParticipation.objects.filter(participant=first_place) or SoloParticipation.objects.filter(participant=second_place)):
                return Response({"message":"invalid ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            SoloWinnerModel.objects.create(
                event = event,
                first = first_place,
                second = second_place
            )
        else:
            event = TeamEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            first_place = TeamModel.objects.get(id=first_id)
            second_place = TeamModel.objects.get(id=second_id)
            if not (TeamParticipation.objects.filter(team=first_place) or TeamParticipation.objects.filter(team=second_place)):
                return Response({"message":"invalid ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            TeamWinnerModel.objects.create(
                event = event,
                first = first_place,
                second = second_place
            )
        return Response({"message":"Winners Added"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

@api_view(["POST"])
def notifyAllParticipants(request):
    try:
        ser = SpecialEmailSerializer(data=request.data)
        if ser.is_valid():
            recievers_list = ParticipantsModel.objects.all().values_list("email", flat=True)
            thread_obj = send_special_email(ser.data["sub"], ser.data["body"], recievers_list)
            thread_obj.start()
            return Response({"message":"Email Sent to all participants"}, status=status.HTTP_200_OK)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def generateParticipationCertificates(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        if not OrganisersModel.objects.filter(email=request.user).first():
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        org = OrganisersModel.objects.get(email=request.user)
        res = checkTeamEvent(org)
        li = []
        if not res:
            event = SoloEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            objs = SoloParticipation.objects.filter(event=event, has_attended=True)
            for obj in objs:
                file_name = generateCertificate(event.title, obj.participant.name, obj.participant.id)
                li.append(file_name)
                thread_obj = send_certificates(obj.participant.email, file_name)
                thread_obj.start()
        else:
            event = TeamEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            objs = TeamParticipation.objects.filter(event=event, has_attended=True)
            for obj in objs:
                file_name = generateCertificate(event.title, obj.team.leader.name, obj.team.leader.id)
                li.append(file_name)
                for i in obj.team.members.all():
                    file_name_2 = generateCertificate(event.title, i.name, i.id)
                    li.append(file_name_2)
                    thread_obj_1 = send_certificates(event.title, i.email, file_name_2)
                    thread_obj_1.start()
                thread_obj = send_certificates(obj.team.leader.email, file_name)
                thread_obj.start()
        li = list(dict.fromkeys(li))
        combineCertificates(li, event.organiser.id, event.organiser.email)
        return Response({"message":"Certificates Sent"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def generateWinnerCertificates(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        if not OrganisersModel.objects.filter(email=request.user).first():
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        org = OrganisersModel.objects.get(email=request.user)
        res = checkTeamEvent(org)
        li = []
        if not res:
            event = SoloEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            obj = SoloWinnerModel.objects.get(event=event)
            f1 = generateWinnerCertificate(event.title, obj.first.name, obj.first.id, "first")
            li.append(f1)
            thread_obj = send_certificates(obj.first.email, f1)
            thread_obj.start()
            f2 = generateWinnerCertificate(event.title, obj.second.name, obj.second.id, "second")
            li.append(f2)
            thread_obj = send_certificates(obj.second.email, f2)
            thread_obj.start()
        else:
            event = TeamEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            obj = TeamWinnerModel.objects.get(event=event)
            f1 = generateWinnerCertificate(event.title, obj.first.leader.name, obj.first.leader.id, "first")
            li.append(f1)
            thread_obj1 = send_certificates(obj.first.leader.email, f1)
            thread_obj1.start()
            f2 = generateWinnerCertificate(event.title, obj.second.leader.name, obj.second.leader.id, "second")
            li.append(f2)
            thread_obj2 = send_certificates(obj.second.leader.email, f2)
            thread_obj2.start()
            for i,j in zip(obj.first.members.all(), obj.second.members.all()):
                f1 = generateWinnerCertificate(event.title, i.name, i.id, "first")
                li.append(f1)
                thread_obj_1 = send_certificates(i.email, f1)
                thread_obj_1.start()
                f2 = generateWinnerCertificate(event.title, j.name, j.id, "second")
                li.append(f2)
                thread_obj_2 = send_certificates(j.email, f2)
                thread_obj_2.start()
        li = list(dict.fromkeys(li))
        combineCertificates(li, event.organiser.id, event.organiser.email)
        return Response({"message":"Certificates Sent"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def attendance(request):
    try:
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        if not OrganisersModel.objects.filter(email=request.user).first():
            return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        org = OrganisersModel.objects.get(email=request.user)
        ser = IDSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        res = checkTeamEvent(org)
        if not res:
            event = SoloEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            if not ParticipantsModel.objects.filter(id=ser.data["id"]):
                return Response({"message":"Invalid ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            obj = SoloParticipation.objects.get(participant=ParticipantsModel.objects.get(id=ser.data["id"]))
            obj.has_attended = True
            obj.save()
        else:
            event = TeamEventModel.objects.get(organiser=org)
            if not event:
                return Response({"message":"You Dont have rights to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            if not TeamModel.objects.filter(id=ser.data["id"]):
                return Response({"message":"Invalid ID"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            obj = TeamParticipation.objects.get(team=TeamModel.objects.get(id=ser.data["id"]))
            obj.has_attended = True
            obj.save()
        return Response({"message":"Attendance Marked"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

