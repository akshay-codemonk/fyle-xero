from django.contrib import admin

from apps.schedule.models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    """
    Admin options for Schedule Model
    """
    list_display = ('id', 'enabled', 'updated_at')
    list_filter = ['enabled', 'created_at', 'updated_at']


# Register Schedule model with admin
admin.site.register(Schedule, ScheduleAdmin)
