from django.urls import path

from apps.fyle_expense.views import ExpenseGroupTriggerView, InvoiceTriggerView

urlpatterns = [
    path('trigger/', ExpenseGroupTriggerView.as_view(), name='expense_group_trigger'),
    path('<group_id>/invoice/trigger/', InvoiceTriggerView.as_view(), name='invoice_trigger')
]
