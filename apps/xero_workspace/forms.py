from django import forms


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
    category_name = forms.CharField(max_length=50, label='', help_text=None,
                                    widget=forms.TextInput(attrs={'placeholder': 'Category Name (Fyle)'}))
    account_code = forms.IntegerField(label='', help_text=None,
                                      widget=forms.NumberInput(attrs={'placeholder': 'Account Code (Xero)'}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class EmployeeMappingForm(forms.Form):
    """
    Form for getting employee mapping key and value
    """
    employee_name = forms.CharField(max_length=50, label='', help_text=None,
                                    widget=forms.TextInput(attrs={'placeholder': 'Employee Name (Fyle)'}))
    contact_email = forms.CharField(label='', help_text=None,
                                    widget=forms.TextInput(attrs={'placeholder': 'Contact Email (Xero)'}))
    bulk_upload_file = forms.FileField(label='', help_text=None,
                                       widget=forms.FileInput(attrs={'accept': '.xlsx'}))


class TransformForm(forms.Form):
    """
    Form for writing sql queries
    """

    def __init__(self, *args, **kwargs):
        super(TransformForm, self).__init__(*args, **kwargs)
        self.fields['transform_sql'].initial = 'This is default text.'

    transform_sql = forms.CharField(label=None, help_text=None,
                                    widget=forms.Textarea(attrs={"rows": 6, "columns": 5, "class": "form-control",
                                                                 "disabled": "True"}))
    test_sql = forms.CharField(label=None, help_text=None,
                               widget=forms.Textarea(attrs={"rows": 6, "columns": 5, "class": "form-control"}))
