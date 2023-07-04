from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        valid_form = form.is_valid()
        print(f'Valid form: {valid_form}')
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            new_user = User.objects.create_user(username=username, password=password, email=email)
            new_user.save()
        else:
            #print(form)
            pass       
        return redirect("/home")
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {"form":form})