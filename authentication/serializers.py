from rest_framework import serializers
from .models import *
from .validators import validate_pw, validate_name


class loginSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    password = serializers.CharField(required = True)


class signupSerializer(serializers.Serializer):
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required = True)
    phone = serializers.IntegerField(required = False)
    password = serializers.CharField(required = True)
    # def validate(self, data):
    #     validate_pw(data["password"])
    #     validate_name(data["name"])
    #     return data


class otpSerializer(serializers.Serializer):
    otp = serializers.CharField(required = True)
    pw = serializers.CharField(required = True)
    def validate(self, data):
        validate_pw(data["pw"])
        return data

class CollegesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeModel
        exclude = ["created_at", "updated_at"]



class emailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)


class AddOrganiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOrganiserModel
        fields = ["file"]


class GetOrganiserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisersModel
        fields = ["name", "phone", "photo"]


class AddTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamModel
        fields = "__all__"


class ParticipantDisplaySerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantsModel
        fields = ["id", "name", "email", "phone"]


class TeamDisplaySerilizer(serializers.ModelSerializer):
    leader = ParticipantDisplaySerilaizer()
    members = ParticipantDisplaySerilaizer(read_only=True, many=True)
    class Meta:
        model = TeamModel
        fields = ["id", "leader", "name", "team_username", "members"]


class SetWinnersSerializer(serializers.Serializer):
    first = serializers.CharField(required = True)
    second = serializers.CharField(required = True)

