import datetime
from django import forms
from .models import Client, Security, Investment, Deposit, QuoteHistory
from django.forms import ModelForm
from django.core.exceptions import ValidationError

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class SecurityForm(forms.ModelForm):
    class Meta:
        model = Security
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuoteHistory
        fields = ['quote', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'quote': forms.NumberInput(attrs={'step': '0.01'})
        }
from django.utils import timezone
class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        fields = '__all__'
        widgets = {
            'security': forms.Select(attrs={'id': 'security-select'}),
            'deposit': forms.Select(attrs={'id': 'deposit-select'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'sale_date': forms.DateInput(attrs={'type': 'date', 'required': False}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase_date'].initial = timezone.now().date()
        self.fields['sale_date'].required = False

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['client', 'amount', 'interest_rate', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'ownership_type', 'address', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['client', 'amount', 'interest_rate', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }