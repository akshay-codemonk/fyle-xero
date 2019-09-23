from django import forms

from .models import XeroCredential


class XeroCredentialsForm(forms.ModelForm):
    """
    Form for getting xero credentials
    """

    class Meta:
        model = XeroCredential
        fields = ('pem_file', 'consumer_key')
        widgets = {
            'consumer_key': forms.TextInput(attrs={'placeholder': 'Consumer Key'})
        }
        help_texts = {
            'pem_file': None,
            'consumer_key': None
        }
