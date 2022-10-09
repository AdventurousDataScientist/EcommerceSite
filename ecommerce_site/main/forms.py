from django import forms

class CreateItem(forms.Form):
    name = forms.CharField(label="name", min_length=2, max_length=100, required=True)
    description = forms.CharField(label="description", min_length=2, max_length=300, required=True)
    price = forms.DecimalField(label="enter price")


