from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm): # user creation form with new attributes
    email = forms.EmailField()

    class Meta: # add new fields in user creation form
        model = User # definming that changing user model
        fields = ["username", "email", "password1", "password2"] # parent class doesn't know email field needs to show up, fields show up in order listed here