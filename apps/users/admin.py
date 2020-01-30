from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from apps.users.models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    pass

#admin.site.register(UserProfile,UserAdmin)