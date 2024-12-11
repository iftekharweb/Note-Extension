from .permissions import IsOwner
from .serializers import TopicSerializer, NoteSerializer
from .models import Topic, Note

from rest_framework import permissions, viewsets


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.queryset.filter(topic__user=self.request.user, topic_id=self.kwargs['topic_pk'])

    def perform_create(self, serializer):
        topic = Topic.objects.get(pk=self.kwargs['topic_pk'], user=self.request.user)
        serializer.save(topic=topic)
