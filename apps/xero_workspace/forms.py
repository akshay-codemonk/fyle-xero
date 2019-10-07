from django import forms
from tempus_dominus.widgets import DateTimePicker


class XeroCredentialsForm(forms.Form):
    """
    Form for getting xero credentials
    """
    consumer_key = forms.CharField(max_length=256, label='', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': 'Consumer Key'}))
    pem_file = forms.FileField(label='', help_text=None,
                               widget=forms.FileInput(attrs={'accept': '.pem'}))


class CategoryMappingForm(forms.Form):
    """
    Form for getting category mapping key and value
    """
    category = forms.CharField(max_length=64, label='', help_text=None,
                               widget=forms.TextInput(attrs={'placeholder': 'Category Name (Fyle)'}))
    sub_category = forms.CharField(max_length=64, label='', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': 'Sub-Category Name (Fyle)'}))
    account_code = forms.IntegerField(label='', help_text=None,
                                      widget=forms.NumberInput(attrs={'placeholder': 'Account Code (Xero)'}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class EmployeeMappingForm(forms.Form):
    """
    Form for getting employee mapping key and value
    """
    employee_email = forms.CharField(max_length=64, label='', help_text=None,
                                     widget=forms.TextInput(attrs={'placeholder': 'Employee Email (Fyle)'}))
    contact_name = forms.CharField(max_length=64, label='', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': 'Contact Name (Xero)'}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class TransformForm(forms.Form):
    """
    Form for writing sql queries
    """

    transform_sql = forms.CharField(label=None, help_text=None,
                                    widget=forms.Textarea(attrs={"rows": 6, "columns": 5, "class": "form-control",
                                                                 "disabled": "True"}))
    test_sql = forms.CharField(label=None, help_text=None,
                               widget=forms.Textarea(attrs={"rows": 6, "columns": 5, "class": "form-control"}))


class ScheduleForm(forms.Form):
    """
    Form to get schedule data
    """

    next_run = forms.DateTimeField(widget=DateTimePicker(
        options={
            'useCurrent': True,
            'format': 'YYYY-MM-DD hh:mm a',
        },
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
        }
    ))

    minutes = forms.IntegerField(initial='3', widget=forms.NumberInput(attrs={
        "class": "form-control",
        "placeholder": "in minutes"
    }))
