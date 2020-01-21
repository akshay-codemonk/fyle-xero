"""
xero_connect app URL Configuration
"""

from django.urls import path

from apps.xero_connect.views import DestinationView, XeroConnectView, XeroDisconnectView

urlpatterns = [
    path('', DestinationView.as_view(), name="destination"),
    path('connect/', XeroConnectView.as_view(), name="xero_connect"),
    path('disconnect/', XeroDisconnectView.as_view(), name="xero_disconnect"),
]
