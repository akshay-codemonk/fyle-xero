from django.db import models
from django_q.models import Schedule

from apps.fyle_connect.models import FyleAuth
from apps.sync_activity.models import Activity
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
    activity = models.ForeignKey(Activity, null=True, blank=True, related_name='activities', on_delete=models.CASCADE,
                                 help_text='FK to Activity')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)

    class Meta:
        unique_together = ('workspace', 'activity',)
