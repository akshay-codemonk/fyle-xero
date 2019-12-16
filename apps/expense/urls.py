"""
expense app URL Configuration
"""
from django.urls import path

from apps.expense.views import ExpenseGroupView

urlpatterns = [
    path('', ExpenseGroupView.as_view(), name="expense_groups"),
]
