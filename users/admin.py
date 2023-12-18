from django.contrib import admin

# Register your models here.
from users.models import User


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
