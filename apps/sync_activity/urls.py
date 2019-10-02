"""
sync_activity app URL Configuration
"""
from django.urls import path

from apps.sync_activity.views import SyncActivityView

urlpatterns = [
    path('', SyncActivityView.as_view(), name="activity")
]
