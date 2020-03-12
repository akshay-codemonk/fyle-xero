from django.contrib import admin

from apps.task_log.models import TaskLog


class TaskLogAdmin(admin.ModelAdmin):
    """
    Admin options for TaskLog model
    """
    list_display = ('task_id', 'type', 'status', 'created_at', 'updated_at')
    list_filter = ['task_id', 'type', 'status', 'created_at', 'updated_at']


admin.site.register(TaskLog, TaskLogAdmin)
