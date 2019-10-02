from django.contrib import admin

from apps.sync_activity.models import Activity


class ActivityAdmin(admin.ModelAdmin):
    """
    Admin options for Activity Model
    """
    list_display = ('id', 'status', 'triggered_by', 'created_at', 'updated_at')
    list_filter = ['status', 'triggered_by', 'created_at', 'updated_at']


# Register Activity model with admin
admin.site.register(Activity, ActivityAdmin)
