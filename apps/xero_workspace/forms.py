from django import forms
from tempus_dominus.widgets import DateTimePicker


class XeroCredentialsForm(forms.Form):
    """
    Form for getting xero credentials
    """
    consumer_key = forms.CharField(max_length=256, label='', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': ' '}))
    pem_file = forms.FileField(label='', help_text=None,
                               widget=forms.FileInput(attrs={'accept': '.pem'}))


class CategoryMappingForm(forms.Form):
    """
    Form for getting category mapping key and value
    """
    category = forms.CharField(max_length=64, label='Category*', help_text=None,
                               widget=forms.TextInput(attrs={'placeholder': ' ',
                                                             'autocomplete': 'off'}))
    sub_category = forms.CharField(max_length=64, label='Subcategory', help_text=None, required=False,
                                   widget=forms.TextInput(attrs={'placeholder': ' ',
                                                                 'autocomplete': 'off'}))
    account_code = forms.IntegerField(label='Account Code*', help_text=None,
                                      widget=forms.NumberInput(attrs={'placeholder': ' '}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class EmployeeMappingForm(forms.Form):
    """
    Form for getting employee mapping key and value
    """
    employee_email = forms.CharField(max_length=64, label='', help_text=None,
                                     widget=forms.TextInput(attrs={'placeholder': ' '}))
    contact_name = forms.CharField(max_length=64, label='', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': ' '}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class ProjectMappingForm(forms.Form):
    """
    Form for getting project mapping key and value
    """
    project_name = forms.CharField(max_length=64, label='', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': ' '}))
    tracking_category_name = forms.CharField(max_length=64, label='', help_text=None,
                                             widget=forms.TextInput(attrs={'placeholder': ' '}))
    tracking_category_option = forms.CharField(max_length=64, label='', help_text=None,
                                               widget=forms.TextInput(attrs={'placeholder': ' '}))
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
            'icon_toggle': True
        }
    ))

    minutes = forms.IntegerField(initial='3', widget=forms.NumberInput(attrs={
        'placeholder': 'in minutes'
    }))
