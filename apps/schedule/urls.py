"""
schedule app URL Configuration
"""
from django.urls import path

from apps.schedule.views import ScheduleView

urlpatterns = [
    path('', ScheduleView.as_view(), name="schedule")
]
