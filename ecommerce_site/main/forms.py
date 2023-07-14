from django import forms
from .secure_variables import CREDIT_CARD_NUMBER, EXPIRATION_DATE, CVV
class PaymentForm(forms.Form):
    cc_number = forms.CharField(label='Credit Card Number', empty_value=CREDIT_CARD_NUMBER)
    cc_expiry = forms.CharField(label='Expiration Date', empty_value=EXPIRATION_DATE)
    cc_code = forms.CharField(label='CVV', min_length=3, max_length=3, empty_value=CVV)

class CreateItem(forms.Form):
    name = forms.CharField(label="name", min_length=2, max_length=100, required=True)
    category = forms.CharField(label="category", min_length=2, max_length=100, required=True)
    description = forms.CharField(label="description", min_length=2, max_length=300, required=True)
    price = forms.DecimalField(label="enter price")
    stock = forms.IntegerField(label="enter stock")
    rating = forms.DecimalField(label="enter rating")



class DepositForm(forms.Form):
    balance = forms.DecimalField(max_digits=10, min_value=0.01)

class CreateStoreForm(forms.Form):
    category = forms.CharField(label="category", min_length=2, max_length=100, required=True)
    description = forms.CharField(label="description", min_length=2, max_length=300, required=True)
    name = forms.CharField(label="name", min_length=2, max_length=300, required=True)

    


