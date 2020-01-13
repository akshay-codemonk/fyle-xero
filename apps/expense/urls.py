"""
expense app URL Configuration
"""
from django.urls import path

from apps.expense.views import ExpenseGroupView, ExpenseView

urlpatterns = [
    path('', ExpenseGroupView.as_view(), name="expense_groups"),
    path('<group_id>/expenses/', ExpenseView.as_view(), name='expenses'),
]
