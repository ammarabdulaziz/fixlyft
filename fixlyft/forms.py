from .models import PickUP
from django import forms
from django.core.validators import RegexValidator


class SchedulePickUpForm(forms.ModelForm):
    class Meta:
        model = PickUP
        fields = '__all__'
        exclude = ('timestamp',)
        widgets = {
            'mobileshop': forms.HiddenInput(),
        }

class PhoneForm(forms.Form):
    phone = forms.CharField()

class VerifyForm(forms.Form):
    phone = forms.CharField()
    otp = forms.CharField()