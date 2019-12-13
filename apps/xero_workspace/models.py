import datetime

from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django_q.models import Schedule
from model_utils import Choices

from apps.fyle_connect.models import FyleAuth
from apps.user.models import UserProfile
from fyle_xero_integration_web_app.settings import BASE_DIR


def default_for_json_field():
    return {"mappings": []}


class Workspace(models.Model):
    """
    Workspace for Fyle Xero integration
    """
    id = models.AutoField(primary_key=True, )
    name = models.CharField(max_length=20, help_text='Name of this workspace')
    user = models.ManyToManyField(UserProfile, help_text='Users belonging to this workspace')
    transform_sql = models.TextField(null=True, blank=True, help_text='Transform SQL')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            file_path = '{}/resources/transform.sql'.format(BASE_DIR)
            with open(file_path, 'r') as myfile:
                transform_sql = myfile.read()
                self.transform_sql = transform_sql
        super(Workspace, self).save(force_insert=False, force_update=False, using=None,
                                    update_fields=None)


class EmployeeMapping(models.Model):
    """
    Mapping table for Fyle Employee to Xero Contact
    """
    id = models.AutoField(primary_key=True)
    employee_email = models.EmailField(max_length=255, unique=False, help_text='Email id of the Fyle employee')
    contact_name = models.CharField(max_length=255, help_text='Name of the Xero contact')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, help_text='Workspace this mapping belongs to')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)


class CategoryMapping(models.Model):
    """
    Mapping table for Fyle Category, Sub-category and Xero Account Code
    """
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=64, help_text='Fyle Expense Category')
    sub_category = models.CharField(max_length=64, null=True, help_text='Fyle Expense Sub-Category')
    account_code = models.IntegerField(null=True, blank=True, help_text='Xero Account code')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, help_text='Workspace this mapping belongs to')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)


class ProjectMapping(models.Model):
    """
    Mapping table for Fyle Project, Xero Tracking Category and Tracking Category options
    """
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=64, help_text='Fyle Project Name')
    tracking_category_name = models.CharField(max_length=64, help_text='Xero Tracking Category Name')
    tracking_category_option = models.CharField(max_length=64, help_text='Xero Tracking Category Option')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, help_text='Workspace this mapping belongs to')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)


class XeroCredential(models.Model):
    """
    Xero credentials
    """
    id = models.AutoField(primary_key=True, help_text='id')
    private_key = models.TextField(help_text='Xero Application Private Key')
    consumer_key = models.CharField(max_length=256, help_text='Xero Consumer key')
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


class Activity(models.Model):
    """
    Activity information
    """
    STATUS = Choices('in_progress', 'failed', 'success', 'timeout')
    TRIGGERS = Choices('user', 'schedule', 'api')

    id = models.AutoField(primary_key=True, )
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, help_text='FK to Workspace')
    transform_sql = models.TextField(null=True, blank=True, help_text='Transform SQL')
    sync_db_file_id = models.CharField(max_length=32, null=True, blank=True, help_text='SQLite database file Id')
    status = models.CharField(choices=STATUS, max_length=20, default=STATUS.in_progress,
                              help_text='Current status of the activity')
    triggered_by = models.CharField(choices=TRIGGERS, default=TRIGGERS.user, max_length=20,
                                    help_text='Activity triggered by')
    request_data = models.TextField(null=True, blank=True, help_text='Request data')
    response_data = models.TextField(null=True, blank=True, help_text='Response data')
    error_msg = models.TextField(null=True, blank=True, help_text='Error message for user')  # Rename to display message
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    def update_status(self, message, status):
        """
        Update the Activity status
        :param message:
        :param status:
        """
        self.error_msg = message
        self.status = status
        self.save()


@receiver(pre_delete, sender=WorkspaceSchedule, dispatch_uid='schedule_delete_signal')
def delete_schedule(instance, **kwargs):
    """
    Delete the schedule related to workspace
    """
    instance.schedule.delete()


@receiver(post_save, sender=Workspace, dispatch_uid='workspace_create_signal')
def create_workspace_(instance, created, **kwargs):
    if created:
        schedule = Schedule.objects.create(func='apps.xero_workspace.tasks.sync_xero_scheduled',
                                           hook='apps.xero_workspace.hooks.update_activity_status',
                                           args=instance.id,
                                           schedule_type=Schedule.MINUTES,
                                           repeats=0,
                                           minutes=5,
                                           next_run=datetime.datetime.now()
                                           )
        WorkspaceSchedule.objects.create(workspace=instance, schedule=schedule)
