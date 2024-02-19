from django.contrib import admin
from user_info.models import UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    # fields which are shown when looking at a list of instances
    list_display = ('id', 'user')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email')
    ordering = ('id',)


admin.site.register(UserInfo, UserInfoAdmin)
