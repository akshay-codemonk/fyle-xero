from django.db import models
from model_utils import Choices


class Activity(models.Model):
    """
    Activity information
    """
    STATUS = Choices('in_progress', 'failed', 'success', 'timeout')
    TRIGGERS = Choices('user', 'schedule', 'api')

    id = models.AutoField(primary_key=True, )
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
