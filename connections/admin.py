from django.contrib import admin

# Register your models here.
from connections.models import FriendRequest


class FriendRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(FriendRequest, FriendRequestAdmin)
