from django.db import models

from apps.fyle_expense.models import ExpenseGroup
from apps.xero_workspace.models import Workspace, Invoice


class TaskLog(models.Model):
    """
    Task log model
    """
    id = models.AutoField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE,
                                  help_text="FK to Workspace")
    task_id = models.CharField(max_length=255, null=True, help_text="Fyle job reference")
    type = models.CharField(max_length=64, help_text="Task type")
    expense_group = models.ForeignKey(ExpenseGroup, null=True, blank=True,
                                      on_delete=models.CASCADE, help_text="FK to ExpenseGroup")
    invoice = models.ForeignKey(Invoice, null=True, blank=True,
                                on_delete=models.PROTECT, help_text="FK to Invoice")
    status = models.CharField(max_length=64, null=True, blank=True, help_text="Task status")
    detail = models.TextField(null=True, blank=True, help_text="Task details")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "created_at"
