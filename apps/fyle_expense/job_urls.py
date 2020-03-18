from django.urls import path

from apps.fyle_expense.views import ExpenseGroupTaskView

urlpatterns = [
    path('', ExpenseGroupTaskView.as_view(), name='expense_groups_job')
]
