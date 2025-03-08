from django import forms
from booking.models import Booking

class BookingForm(forms.ModelForm):
    price = forms.DecimalField(label="price", required=False)
    level = forms.IntegerField(label="level", required=False)
    duration = forms.IntegerField(label="duration (min)", required=False)
    status = forms.CharField(label="confirmed", required=False)
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        editable = kwargs.pop('editable', False)
        super().__init__(*args, **kwargs)

        if 'instance' in kwargs and kwargs['instance']:
            booking = kwargs['instance']
            if booking.service:
                self.fields['price'].initial = booking.service.price
                self.fields['level'].initial = booking.service.level
                self.fields['duration'].initial = booking.service.duration

        if not editable:
            self.fields['price'].disabled = True
            self.fields['level'].disabled = True
            self.fields['duration'].disabled = True
            self.fields['user'].disabled = True
            self.fields['trainer'].disabled = True
            self.fields['service'].disabled = True
            self.fields['datetime_start'].disabled = True
            self.fields['datetime_end'].disabled = True
            self.fields['status'].disabled = True
