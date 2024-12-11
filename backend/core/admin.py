from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'name', 'is_admin', 'is_active']
    list_filter = ['is_admin', 'is_active']
    ordering = ['id']

    fieldsets = [
        ['User Info', {'fields': ['email', 'name', 'password']}],
        ['Permissions', {'fields': ['is_admin', 'is_active']}],
    ]

    add_fieldsets = [
        [
            None,
            {
                'classes': ['wide'],
                'fields': ['email', 'name', 'password1', 'password2'],
            },
        ]
    ]

    search_fields = ['email', 'name']
    filter_horizontal = []  
