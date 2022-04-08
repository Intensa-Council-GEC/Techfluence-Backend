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