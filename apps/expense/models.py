from django.db import models

from apps.xero_workspace.models import Workspace


class Expense(models.Model):
    """
    Expense
    """
    id = models.AutoField(primary_key=True)
    employee_email = models.EmailField(max_length=255, unique=False, help_text='Email id of the Fyle employee')
    category = models.CharField(max_length=64, help_text='Fyle Expense Category')
    sub_category = models.CharField(max_length=64, null=True, help_text='Fyle Expense Sub-Category')
    purpose = models.CharField(max_length=64, help_text='Purpose')
    expense_id = models.CharField(max_length=64, unique=True, help_text="Expense ID")
    expense_number = models.CharField(max_length=64, unique=True, help_text="Expense Number")
    amount = models.FloatField(help_text="Amount")
    settlement_id = models.CharField(max_length=64, help_text="Settlement ID")
    report_id = models.CharField(max_length=64, help_text="Report ID")
    project = models.CharField(max_length=64, help_text="Project")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return self.expense_id


class ExpenseGroup(models.Model):
    """
    Expense Group
    """
    id = models.AutoField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.PROTECT,
                                  help_text="To which workspace this expense group belongs to")
    expenses = models.ManyToManyField(Expense, help_text="Expenses under this Expense Group")
    description = models.CharField(max_length=255, help_text="Description")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)
