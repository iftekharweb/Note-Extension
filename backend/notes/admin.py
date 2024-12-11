from django.contrib import admin
from .models import Topic, Note

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user']
    search_fields = ['title', 'user__username']
    list_filter = ['user',]
    ordering = ['id',]
    autocomplete_fields = ['user',] 

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'topic', 'is_favourite']
    search_fields = ['title', 'topic__title']
    list_filter = ['is_favourite', 'topic']
    ordering = ['id',]
    autocomplete_fields = ['topic',]
