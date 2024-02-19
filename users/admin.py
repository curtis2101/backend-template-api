from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    readonly_fields = ('date_joined',)
    # fields which are shown when looking at a list of instances
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'is_staff')
    ordering = ('id',)
