from django import forms
from .models import PhoneRecord

class PhoneRecordForm(forms.ModelForm):
    class Meta:
        model = PhoneRecord
        # Указываем поля, которые разрешено заполнять при создании нового номера
        fields = ['phone_4', 'port_asl', 'stan', 'lin', 'department', 'address', 'status_id']


# forms.py
from django import forms
from .models import DamageRecord, FailureType

class DamageRecordForm(forms.ModelForm):
    class Meta:
        model = DamageRecord
        fields = ['phone_record', 'comment', 'failure_type']

    failure_type = forms.ModelChoiceField(queryset=FailureType.objects.all(), required=False)
