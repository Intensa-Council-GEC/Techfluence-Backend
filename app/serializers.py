from rest_framework import serializers
from authentication.serializers import GetOrganiserDetailsSerializer
from .models import *


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsModel
        fields = "__all__"


class EventSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = EventModel
        fields = ["id", "title", "short_desc", "logo"]


# class RulesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RulesModel
#         fields = ["rule"]


class EventDetailSerislizer(serializers.ModelSerializer):
    organiser = GetOrganiserDetailsSerializer()
    # rules = serializers.SerializerMethodField()
    class Meta:
        model = EventModel
        exclude = ["whats_app", "created_at", "updated_at"]
    # def get_rules(self, obj):
    #     rules = []
    #     try:
    #         event_obj = EventModel.objects.get(id = obj.id)
    #         serializer = RulesSerializer(event_obj.event_rules.all(), many=True)
    #         cart_items = serializer.data
    #         return cart_items
    #     except Exception as e:
    #         print(e)


class SpecialEmailSerializer(serializers.Serializer):
    sub = serializers.CharField(required = True)
    body = serializers.CharField(required = True)


class SoloEventRegistration(serializers.Serializer):
    name = serializers.CharField(required = True)
    phone = serializers.IntegerField(required = True)
    email = serializers.EmailField(required = True)


# class TeamEventRegistration(serializers.Serializer):
    # team_name = 