from django.db import models


class XeroAuth(models.Model):
    """
    Xero (Destination) credentials
    """
    id = models.AutoField(primary_key=True, )
    url = models.URLField(max_length=300, default='https://api.xero.com',
                          help_text='Base URL of the xero environment')
    client_id = models.CharField(max_length=256, help_text='Client Id')
    client_secret = models.CharField(max_length=256, help_text='Client Secret')
    refresh_token = models.CharField(max_length=512, help_text='Refresh Token')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Created at')
    updated_at = models.DateTimeField(auto_now=True, help_text='Updated at')

    def __str__(self):
        return str(self.id)
