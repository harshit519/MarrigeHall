from django import forms
from .models import Booking, TableBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event_type', 'event_date', 'start_time', 'end_time', 'number_of_guests', 'special_requirements']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'special_requirements': forms.Textarea(attrs={'rows': 4}),
        }

class TableBookingForm(forms.ModelForm):
    class Meta:
        model = TableBooking
        fields = ['table_number', 'booking_date', 'booking_time', 'number_of_guests', 'special_requests']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }
