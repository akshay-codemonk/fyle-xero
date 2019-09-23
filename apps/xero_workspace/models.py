from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.fyle_connect.models import FyleAuth
from apps.schedule.models import Schedule
from apps.sync_activity.models import Activity
from apps.user.models import UserProfile


class Workspace(models.Model):
    """
    Workspace for Fyle Xero integration
    """
    id = models.AutoField(primary_key=True, )
    name = models.CharField(max_length=20, help_text='Name of this workspace')
    user = models.ManyToManyField(UserProfile, help_text='Users belonging to this workspace')
    employee_contact = JSONField(null=True, blank=True,
                                 help_text='Fyle Employee email to Xero Contact email mapping')
    category_account = JSONField(null=True, blank=True,
                                 help_text='Fyle Category to Xero Account mapping')
    transform_sql = models.TextField(null=True, blank=True, help_text='Transform SQL')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return self.name


class XeroCredential(models.Model):
    """
    Xero credentials
    """
    id = models.AutoField(primary_key=True, help_text='id')
    pem_file = models.FileField(help_text='Xero pem file')
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
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, help_text='FK to Schedule')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)


class WorkspaceActivity(models.Model):
    """
    Sync activity for Xero workspace  (Intermediate Table)
    """
    id = models.AutoField(primary_key=True, )
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, help_text='FK to Workspace')
    activity = models.ForeignKey(Activity, null=True, blank=True, on_delete=models.CASCADE,
                                 help_text='FK to Activity')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('workspace', 'activity',)
