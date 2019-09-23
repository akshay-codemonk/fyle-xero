"""
fyle_connect app URL Configuration
"""
from django.urls import path

from apps.fyle_connect.views import FyleAuthoriseView

urlpatterns = [
    path('', FyleAuthoriseView.as_view(), name="source")
]
