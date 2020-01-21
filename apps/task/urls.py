"""
task app URL Configuration
"""
from django.urls import path

from apps.task.views import TaskLogView, TaskLogDetailsView

urlpatterns = [
    path('', TaskLogView.as_view(), name="tasks"),
    path('<int:task_log_id>/details/', TaskLogDetailsView.as_view(), name="task_log_details")
]
