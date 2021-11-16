from django import forms 
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields =('service','item','telephone','email','location','description',  )
