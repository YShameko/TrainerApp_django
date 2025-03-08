from django import forms

class ScheduleForm(forms.Form):
    datetime_start = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), label='working hours from')
    datetime_end = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), label='                to')


