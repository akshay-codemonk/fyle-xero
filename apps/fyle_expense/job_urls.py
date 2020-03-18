from django.urls import path

from apps.fyle_expense.views import ExpenseGroupTaskView, InvoiceTaskView

urlpatterns = [
    path('expense_group/trigger/', ExpenseGroupTaskView.as_view(), name='expense_group_trigger'),
    path('invoice/trigger/', InvoiceTaskView.as_view(), name='invoice_trigger')
]
