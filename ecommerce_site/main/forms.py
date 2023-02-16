from django import forms
from .secure_variables import CREDIT_CARD_NUMBER, CVV, EXPIRATION_DATE

class PaymentForm(forms.Form):
    cc_number = forms.CharField(label='credit_card_number', empty_value=CREDIT_CARD_NUMBER)
    cc_expiry = forms.CharField(label='expiration_date', empty_value=EXPIRATION_DATE)
    cc_code = forms.CharField(label='cvv', min_length=3, max_length=3, empty_value=CVV)

class CreateItem(forms.Form):
    name = forms.CharField(label="name", min_length=2, max_length=100, required=True)
    description = forms.CharField(label="description", min_length=2, max_length=300, required=True)
    price = forms.DecimalField(label="enter price")




