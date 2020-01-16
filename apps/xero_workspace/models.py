import datetime
import json

import pytz
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django_q.models import Schedule

from apps.fyle_connect.models import FyleAuth
from apps.user.models import UserProfile
from apps.xero_connect.models import XeroAuth


def default_for_json_field():
    return {"mappings": []}


class Workspace(models.Model):
    """
    Workspace for Fyle Xero integration
    """
    id = models.AutoField(primary_key=True, )
    name = models.CharField(max_length=20, help_text='Name of this workspace')
    user = models.ManyToManyField(UserProfile, help_text='Users belonging to this workspace')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return self.name


class EmployeeMapping(models.Model):
    """
    Mapping table for Fyle Employee to Xero Contact
    """
    id = models.AutoField(primary_key=True)
    employee_email = models.EmailField(max_length=255, unique=False, help_text='Email id of the Fyle employee')
    contact_name = models.CharField(max_length=255, help_text='Name of the Xero contact')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, help_text='Workspace this mapping belongs to')
    invalid = models.BooleanField(default=False, help_text='Indicates if this mapping is invalid')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]


class CategoryMapping(models.Model):
    """
    Mapping table for Fyle Category, Sub-category and Xero Account Code
    """
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=64, help_text='Fyle Expense Category')
    sub_category = models.CharField(max_length=64, null=True, help_text='Fyle Expense Sub-Category')
    account_code = models.IntegerField(null=True, blank=True, help_text='Xero Account code')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, help_text='Workspace this mapping belongs to')
    invalid = models.BooleanField(default=False, help_text='Indicates if this mapping is invalid')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]


class ProjectMapping(models.Model):
    """
    Mapping table for Fyle Project, Xero Tracking Category and Tracking Category options
    """
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=64, help_text='Fyle Project Name')
    tracking_category_name = models.CharField(max_length=64, help_text='Xero Tracking Category Name')
    tracking_category_option = models.CharField(max_length=64, help_text='Xero Tracking Category Option')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, help_text='Workspace this mapping belongs to')
    invalid = models.BooleanField(default=False, help_text='Indicates if this mapping is invalid')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created_at"]


class XeroCredential(models.Model):
    """
    Xero credentials
    """
    id = models.AutoField(primary_key=True, help_text='id')
    xero_auth = models.OneToOneField(XeroAuth, on_delete=models.CASCADE,
                                     help_text='FK to Xero Auth')
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, help_text='Workspace')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)


class FyleCredential(models.Model):
    """
    Workspace Fyle Credentials  (Intermediate Table)
    """
    id = models.AutoField(primary_key=True, )
    fyle_auth = models.OneToOneField(FyleAuth, on_delete=models.CASCADE,
                                     help_text='FK to Fyle Auth')
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE,
                                     help_text='FK to Workspace')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)


class WorkspaceSchedule(models.Model):
    """
    Schedule for Xero workspace (Intermediate Table)
    """
    id = models.AutoField(primary_key=True, )
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE,
                                     help_text='FK to Workspace')
    schedule = models.OneToOneField(Schedule, null=True, on_delete=models.SET_NULL, help_text='FK to Schedule')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)


@receiver(pre_delete, sender=WorkspaceSchedule, dispatch_uid='schedule_delete_signal')
def delete_schedule(instance, **kwargs):
    """
    Delete the schedule related to workspace
    """
    instance.schedule.delete()


@receiver(post_save, sender=Workspace, dispatch_uid='workspace_create_signal')
def create_workspace_(instance, created, **kwargs):
    if created:
        kwargs = {"workspace_id": instance.id}
        schedule = Schedule.objects.create(func='apps.task.tasks.create_task',
                                           schedule_type=Schedule.MINUTES,
                                           repeats=0,
                                           minutes=5,
                                           next_run=datetime.datetime.now(tz=pytz.UTC),
                                           kwargs={"workspace_id": instance.id}
                                           )
        WorkspaceSchedule.objects.create(workspace=instance, schedule=schedule)


class Invoice(models.Model):
    """
    Invoice model
    """
    id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=64, help_text="Invoice number")
    invoice_id = models.CharField(max_length=64, null=True, blank=True, help_text="Invoice id")
    contact_name = models.CharField(max_length=64, help_text="Contact Name")
    date = models.DateTimeField(help_text="Invoice created date")
    due_date = models.DateTimeField(null=True, blank=True, help_text="Invoice due date")
    description = models.CharField(max_length=64, help_text="Description")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    @staticmethod
    def create_invoice(expense_group):
        """
        Create invoice from expense group
        :param expense_group
        :return: invoice id
        """
        description = json.loads(expense_group.description)
        try:
            invoice = Invoice.objects.create(
                invoice_number=description.get("report_id"),
                description=description.get("report_id"),
                contact_name=EmployeeMapping.objects.get(
                    employee_email=description.get("employee_email")).contact_name,
                date=description.get("approved_at")
            )
            return invoice.id
        except EmployeeMapping.DoesNotExist:
            EmployeeMapping.objects.create(workspace=expense_group.workspace,
                                           employee_email=description.get("employee_email"), invalid=True)
            raise EmployeeMapping.DoesNotExist


class InvoiceLineItem(models.Model):
    """
    Invoice line item model
    """
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,
                                related_name="invoice_line_items", help_text="FK to Invoice")
    account_code = models.IntegerField(help_text="Account Code")
    account_name = models.CharField(max_length=64, help_text="Account name")
    description = models.CharField(max_length=64, help_text="Description")
    amount = models.FloatField(help_text="Invoice line item amount")
    tracking_category_name = models.CharField(max_length=64, null=True, blank=True,
                                              help_text="Tracking Category Name")
    tracking_category_option = models.CharField(max_length=64, null=True, blank=True,
                                                help_text="Tracking Category Option")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    @staticmethod
    def delete_invoice(expense_group):
        """
        Delete invoice and it's line items
        """
        invoice_id = expense_group.invoice.id
        expense_group.invoice = None
        expense_group.save()
        for expense in expense_group.expenses.all():
            expense.invoice_line_item = None
            expense.save()
        Invoice.objects.filter(id=invoice_id).delete()

    @staticmethod
    def create_invoice_line_item(invoice_id, expense_group):
        """
        Create Invoice line item from expenses and update ExpenseGroup
        and Expense model fields
        :param invoice_id
        :param expense_group
        """
        expenses = expense_group.expenses.all()
        for expense in expenses:
            try:
                invoice_line_item = InvoiceLineItem.objects.create(
                    invoice=Invoice.objects.get(id=invoice_id),
                    account_code=CategoryMapping.objects.get(
                        workspace=expense_group.workspace,
                        category=expense.category).account_code,
                    account_name="",
                    description=expense.report_id,
                    amount=expense.amount
                )
            except CategoryMapping.DoesNotExist:
                CategoryMapping.objects.create(workspace=expense_group.workspace, category=expense.category,
                                               sub_category=expense.sub_category,
                                               invalid=True)
                InvoiceLineItem.delete_invoice(expense_group)
                raise CategoryMapping.DoesNotExist

            if expense.project is not None:
                try:
                    project_mapping = ProjectMapping.objects.get(workspace=expense_group.workspace,
                                                                 project_name=expense.project)
                    invoice_line_item.tracking_category_name = project_mapping.tracking_category_name
                    invoice_line_item.tracking_category_option = project_mapping.tracking_category_option
                    invoice_line_item.save()
                except ProjectMapping.DoesNotExist:
                    ProjectMapping.objects.create(workspace=expense_group.workspace, project_name=expense.project,
                                                  invalid=True)
                    InvoiceLineItem.delete_invoice(expense_group)
                    raise ProjectMapping.DoesNotExist

            if invoice_line_item.id:
                expense.invoice_line_item = InvoiceLineItem.objects.get(
                    id=invoice_line_item.id)
                expense.save()
                expense_group.invoice = Invoice.objects.get(id=invoice_id)
                expense_group.save()
