from django.contrib import admin

from apps.task_log.models import TaskLog


class TaskLogAdmin(admin.ModelAdmin):
    """
    Admin options for TaskLog model
    """
    list_display = ('id', 'level', 'created_at', 'updated_at')
    list_filter = ['level', 'created_at', 'updated_at']


admin.site.register(TaskLog, TaskLogAdmin)
