from django.db import models
from core.models import User

class Topic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Note(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    note = models.TextField()
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.title
