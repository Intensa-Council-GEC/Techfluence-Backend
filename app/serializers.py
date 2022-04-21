from rest_framework import serializers
from authentication.serializers import *
from .models import *


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = "__all__"


class SoloEventSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = SoloEventModel
        fields = ["id", "title", "short_desc", "logo"]
class TeamEventSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = TeamEventModel
        fields = ["id", "title", "short_desc", "logo"]


class SoloEventRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoloEventRulesModel
        fields = ["rule"]
class TeamEventRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamEventRulesModel
        fields = ["rule"]


class SoloEventDetailSerislizer(serializers.ModelSerializer):
    organiser = GetOrganiserDetailsSerializer()
    rules = serializers.SerializerMethodField()
    class Meta:
        model = SoloEventModel
        exclude = ["created_at", "updated_at"]
    def get_rules(self, obj):
        rules = []
        try:
            event_obj = EventModel.objects.get(id = obj.id)
            serializer = SoloEventRulesSerializer(event_obj.event_rules.all(), many=True)
            cart_items = serializer.data
            return cart_items
        except Exception as e:
            print(e)
class TeamEventDetailSerislizer(serializers.ModelSerializer):
    organiser = GetOrganiserDetailsSerializer()
    rules = serializers.SerializerMethodField()
    class Meta:
        model = TeamEventModel
        exclude = ["created_at", "updated_at"]
    def get_rules(self, obj):
        rules = []
        try:
            event_obj = EventModel.objects.get(id = obj.id)
            serializer = TeamEventRulesSerializer(event_obj.event_rules.all(), many=True)
            cart_items = serializer.data
            return cart_items
        except Exception as e:
            print(e)


class SpecialEmailSerializer(serializers.Serializer):
    sub = serializers.CharField(required = True)
    body = serializers.CharField(required = True)


class SoloEventRegistration(serializers.Serializer):
    name = serializers.CharField(required = True)
    college = serializers.CharField(required = True)
    phone = serializers.IntegerField(required = True)
    email = serializers.EmailField(required = True)


class TeamEventRegistration(serializers.Serializer):
    team_name = serializers.CharField(required = True)
    team_username = serializers.CharField(required = True)
    leader_name = serializers.CharField(required = True)
    leader_email = serializers.EmailField(required = True)
    leader_phone = serializers.IntegerField(required = True)
    college = serializers.CharField(required = True)
    memer_1_name = serializers.CharField(required = True)
    memer_1_email = serializers.EmailField(required = True)
    memer_1_phone = serializers.IntegerField(required = True)
    memer_2_name = serializers.CharField(required = False)
    memer_2_email = serializers.EmailField(required = False)
    memer_2_phone = serializers.IntegerField(required = False)
    memer_3_name = serializers.CharField(required = False)
    memer_3_email = serializers.EmailField(required = False)
    memer_3_phone = serializers.IntegerField(required = False)
    memer_4_name = serializers.CharField(required = False)
    memer_4_email = serializers.EmailField(required = False)
    memer_4_phone = serializers.IntegerField(required = False)
    memer_5_name = serializers.CharField(required = False)
    memer_5_email = serializers.EmailField(required = False)
    memer_5_phone = serializers.IntegerField(required = False)
    memer_6_name = serializers.CharField(required = False)
    memer_6_email = serializers.EmailField(required = False)
    memer_6_phone = serializers.IntegerField(required = False)
    memer_7_name = serializers.CharField(required = False)
    memer_7_email = serializers.EmailField(required = False)
    memer_7_phone = serializers.IntegerField(required = False)


class SoloEventParticipantsListSerializer(serializers.ModelSerializer):
    participant = ParticipantDisplaySerilaizer()
    class Meta:
        model = SoloParticipation
        fields = ["participant"]


class TeamEventParticipantsListSerializer(serializers.ModelSerializer):
    team = TeamDisplaySerilizer()
    class Meta:
        model = TeamParticipation
        fields = ["team"]