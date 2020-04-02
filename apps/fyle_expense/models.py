from itertools import groupby

from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.xero_workspace.models import Workspace, InvoiceLineItem, Invoice
from apps.xero_workspace.utils import connect_to_fyle


class Expense(models.Model):
    """
    Expense
    """
    id = models.AutoField(primary_key=True)
    employee_email = models.EmailField(max_length=255, unique=False, help_text='Email id of the Fyle employee')
    category = models.CharField(max_length=255, null=True, blank=True, help_text='Fyle Expense Category')
    sub_category = models.CharField(max_length=255, null=True, blank=True, help_text='Fyle Expense Sub-Category')
    vendor = models.CharField(max_length=255, null=True, blank=True, help_text="Vendor")
    purpose = models.TextField(null=True, blank=True, help_text='Purpose')
    expense_id = models.CharField(max_length=255, unique=True, help_text="Expense ID")
    expense_number = models.CharField(max_length=255, help_text="Expense Number")
    amount = models.FloatField(help_text="Amount")
    settlement_id = models.CharField(max_length=255, help_text="Settlement ID")
    report_id = models.CharField(max_length=255, help_text="Report ID")
    project = models.CharField(max_length=255, null=True, blank=True, help_text="Project")
    expense_created_at = models.DateTimeField(help_text="Expense created at")
    spent_at = models.DateTimeField(help_text="Expense spent at")
    reimbursable = models.BooleanField(help_text="Expense reimbursable or not")
    state = models.CharField(max_length=255, help_text="Expense state")
    invoice_line_item = models.ForeignKey(InvoiceLineItem, null=True, blank=True,
                                          on_delete=models.PROTECT, help_text="FK to InvoiceLineItem")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return self.expense_id

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "created_at"

    @staticmethod
    def fetch_paid_expenses(workspace_id, updated_at):
        """
        Fetch expenses from Fyle API filtered by state and updated_at
        """
        connection = connect_to_fyle(workspace_id)
        if updated_at is None:
            expenses = connection.Expenses.get(state='PAID')
        else:
            expenses = connection.Expenses.get(
                state='PAID',
                updated_at=f'gte:{updated_at.strftime("%Y-%m-%dT%H:%M:%S.%-SZ")}'
            )
        return expenses

    @staticmethod
    def create_expense_objects(expenses):
        """
        Bulk create expense objects
        """
        expense_objects = [Expense(
            employee_email=expense['employee_email'],
            category=expense['category_name'],
            sub_category=expense['sub_category'],
            vendor=expense['vendor'],
            purpose=expense['purpose'],
            expense_id=expense['id'],
            expense_number=expense['expense_number'],
            amount=expense['amount'],
            settlement_id=expense['settlement_id'],
            report_id=expense['report_id'],
            project=expense['project_name'],
            expense_created_at=expense['created_at'],
            spent_at=expense['spent_at'],
            reimbursable=expense['reimbursable'],
            state=expense['state']
        ) for expense in expenses['data']]

        expense_objects = Expense.objects.bulk_create(expense_objects)
        return expense_objects


class ExpenseGroup(models.Model):
    """
    Expense Group
    """
    id = models.AutoField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE,
                                  help_text="To which workspace this expense group belongs to")
    expenses = models.ManyToManyField(Expense, help_text="Expenses under this Expense Group")
    invoice = models.ForeignKey(Invoice, null=True, blank=True,
                                on_delete=models.PROTECT, help_text="FK to Invoice")
    description = JSONField(default=dict, help_text="Description")
    status = models.CharField(max_length=10, help_text="Status")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]
        get_latest_by = "created_at"

    @staticmethod
    def group_expense_by_report_id(expense_objects, workspace_id, connection):
        """
        Group expense by report_id
        """
        expense_groups = []
        reports = connection.Reports.get(state='PAID')
        for report_id, _expense_group in groupby(expense_objects, key=lambda x: x.report_id):
            report = [report for report in reports['data'] if report_id == report['id']].pop()
            report_data = {
                "report_id": report['id'],
                "employee_email": report['employee_email'],
                "approved_at": report['approved_at']
            }
            expense_groups.append(ExpenseGroup(
                workspace=Workspace.objects.get(id=workspace_id),
                description=report_data
            ))
        return expense_groups

    @staticmethod
    def create_expense_groups(expense_groups):
        expense_group_objects = ExpenseGroup.objects.bulk_create(expense_groups)
        through_model_objects = []
        for expense_group_object in expense_group_objects:
            report_id = expense_group_object.description['report_id']
            expenses = Expense.objects.filter(report_id=report_id)
            for expense in expenses:
                through_model_objects.append(ExpenseGroup.expenses.through(
                    expensegroup_id=expense_group_object.id,
                    expense_id=expense.id
                ))
        ExpenseGroup.expenses.through.objects.bulk_create(through_model_objects)
        return expense_group_objects
