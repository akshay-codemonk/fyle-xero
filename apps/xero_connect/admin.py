from django.contrib import admin

from apps.xero_connect.models import XeroAuth


class XeroAuthAdmin(admin.ModelAdmin):
    """
    Admin options for XeroAuth Model
    """
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']


# Register XeroAuth model with admin
admin.site.register(XeroAuth, XeroAuthAdmin)
