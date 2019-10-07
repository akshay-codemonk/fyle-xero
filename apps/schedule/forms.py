from django import forms
from tempus_dominus.widgets import DateTimePicker


class ScheduleForm(forms.Form):
    """
    Form to get schedule data
    """

    start_at = forms.DateTimeField(widget=DateTimePicker(
        options={
            'useCurrent': True,
            'format': 'YYYY-MM-DD hh:mm a',
        },
        attrs={
            'append': 'fa fa-calendar',
            'icon_toggle': True,
        }
    ))

    time_interval = forms.IntegerField(initial='3', widget=forms.NumberInput(attrs={
        "class": "form-control",
        "placeholder": "in minutes"
    }))
