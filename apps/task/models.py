from django.db import models
from django_q.models import Task

from apps.expense.models import ExpenseGroup
from apps.xero_workspace.models import Workspace, Invoice


class TaskLog(models.Model):
    """
    Task log model
    """
    id = models.AutoField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT,
                                  help_text="FK to Workspace")
    task = models.ForeignKey(Task, on_delete=models.PROTECT, help_text="FK to Task")
    expense_group = models.ForeignKey(ExpenseGroup, null=True, blank=True,
                                      on_delete=models.PROTECT, help_text="FK to ExpenseGroup")
    invoice = models.ForeignKey(Invoice, null=True, blank=True,
                                on_delete=models.PROTECT, help_text="FK to Invoice")
    level = models.CharField(max_length=64, help_text="Level")
    detail = models.TextField(help_text="Detail")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)
