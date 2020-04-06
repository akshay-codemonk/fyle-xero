from django import forms
from tempus_dominus.widgets import DateTimePicker


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
    account_code = forms.CharField(max_length=32, label='Account Code*', help_text=None,
                                   widget=forms.NumberInput(attrs={'placeholder': ' '}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class EmployeeMappingForm(forms.Form):
    """
    Form for getting employee mapping key and value
    """
    employee_email = forms.CharField(max_length=64, label='Employee Email*', help_text=None,
                                     widget=forms.TextInput(attrs={'placeholder': ' ',
                                                                   'autocomplete': 'off'}))
    contact_name = forms.CharField(max_length=64, label='Contact Name*', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': ' ',
                                                                 'autocomplete': 'off'}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class ProjectMappingForm(forms.Form):
    """
    Form for getting project mapping key and value
    """
    project_name = forms.CharField(max_length=64, label='Project Name*', help_text=None,
                                   widget=forms.TextInput(attrs={'placeholder': ' ',
                                                                 'autocomplete': 'off'}))
    tracking_category_name = forms.CharField(max_length=64, label='Tracking Category Name*',
                                             help_text=None,
                                             widget=forms.TextInput(attrs={'placeholder': ' ',
                                                                           'autocomplete': 'off'}))
    tracking_category_option = forms.CharField(max_length=64, label='Tracking Category Option*',
                                               help_text=None,
                                               widget=forms.TextInput(attrs={'placeholder': ' ',
                                                                             'autocomplete': 'off'}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class ScheduleForm(forms.Form):
    """
    Form to get schedule data
    """

    start_datetime = forms.DateTimeField(widget=DateTimePicker(
        options={
            'useCurrent': True,
            'format': 'YYYY-MM-DD hh:mm a',
        },
        attrs={
            'icon_toggle': True
        }
    ))

    hours = forms.IntegerField(initial='3', widget=forms.NumberInput(attrs={
        'placeholder': 'in hours'
    }))
