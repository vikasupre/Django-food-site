from django.contrib import admin
from accounts.models import User,UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_filter=()
    filter_horizontal=()
    fieldsets=()
    list_display=['email','username','first_name','last_name','role','is_staff','is_active']
    ordering=('-date_created',)

admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)

# Register your models here.
