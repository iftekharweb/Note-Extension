
from rest_framework import serializers
from . import models

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Note
        fields = ['id', 'title', 'is_favourite', 'topic']
        read_only_fields = ['topic']

class TopicSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)

    class Meta:
        model = models.Topic
        fields = ['id', 'title', 'notes', 'user']
        read_only_fields = ['user']