"""
expense app URL Configuration
"""
from django.urls import path

from apps.fyle_expense.views import ExpenseGroupView, ExpenseView, InvoiceDetailsView, ExpenseDetailsView, \
    ExpenseGroupTaskView

urlpatterns = [
    path('', ExpenseGroupView.as_view(), name="expense_groups"),
    path('<int:group_id>/expenses/', ExpenseView.as_view(), name='expenses'),
    path('<int:group_id>/expenses/<int:expense_id>/details/', ExpenseDetailsView.as_view(),
         name='expenses_details'),
    path('<int:group_id>/invoice/', InvoiceDetailsView.as_view(), name='invoice'),
    path('task/', ExpenseGroupTaskView.as_view(), name='expense_groups_task')
]
