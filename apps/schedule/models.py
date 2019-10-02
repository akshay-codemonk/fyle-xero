from django.db import models


class Schedule(models.Model):
    """
    Model for storing Schedules
    """
    id = models.AutoField(primary_key=True, )
    start_at = models.DateTimeField(help_text='Schedule start at')
    enabled = models.BooleanField(default=False, help_text='Schedule enabled')
    time_interval = models.IntegerField(help_text="Time interval between successive sync's in minutes")
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)
