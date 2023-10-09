from django.contrib import admin
from .models import Vendor

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display=['user','vendor_name','is_approved']
    list_display_links=['user','vendor_name']

admin.site.register(Vendor,VendorAdmin)
