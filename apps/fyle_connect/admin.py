from django.contrib import admin

from apps.fyle_connect.models import FyleAuth


class FyleAuthAdmin(admin.ModelAdmin):
    """
    Admin options for FyleAuth Model
    """
    list_display = ('id', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']


# Register FyleAuth model with admin
admin.site.register(FyleAuth, FyleAuthAdmin)
