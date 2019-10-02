"""
fyle_connect app URL Configuration
"""
from django.urls import path

from apps.fyle_connect.views import FyleConnectView, FyleDisconnectView, SourceView

urlpatterns = [
    path('', SourceView.as_view(), name="source"),
    path('connect/', FyleConnectView.as_view(), name="fyle_connect"),
    path('disconnect/', FyleDisconnectView.as_view(), name="fyle_disconnect"),
]
