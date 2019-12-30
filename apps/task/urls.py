"""
task app URL Configuration
"""
from django.urls import path

from apps.task.views import TaskLogView

urlpatterns = [
    path('', TaskLogView.as_view(), name="tasks"),
]