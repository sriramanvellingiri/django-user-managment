from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Events,FileUpload
from django.db import transaction


class ParticipantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['id']


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = '__all__'
        depth = 1

    def to_representation(self, data):
        ret = super().to_representation(data)
        return ret

class EventCreateUpdateSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True,required=True)

    class Meta:
        model = Events
        fields = ('id','type','start_date','end_date','participants','city')

    @transaction.atomic()
    def create(self, validated_data):
        participant_data = validated_data.pop('participants')
        validated_data['created_by'] = self.context['request'].user
        event_obj = Events.objects.create(**validated_data)
        for participant in participant_data:
            event_obj.participants.add(participant.get('id'))
        return event_obj

    @transaction.atomic()
    def update(self, instance, validated_data):
        participant_data = validated_data.pop('participants')
        instance.type = validated_data.get('type',instance.type)
        instance.start_date = validated_data.get('start_date',instance.start_date)
        instance.end_date = validated_data.get('end_date',instance.end_date)
        instance.city = validated_data.get('city',instance.city)
        instance.participants.clear()
        for participant in participant_data:
            instance.participants.add(participant.get('id'))
        instance.save()
        return instance

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileUpload
        fields = "__all__"
