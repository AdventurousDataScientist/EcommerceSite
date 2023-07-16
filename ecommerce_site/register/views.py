from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        valid_form = form.is_valid()
        print(f'Valid form: {valid_form}')
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            if not User.objects.filter(username=username).first():
                form.save()
                messages.info(request, "Thanks for registering. You are now logged in.")
                new_user = authenticate(username=username,
                                        password=password,
                                        )
                login(request, new_user)
                print(f'Authenticated after Registration?: {request.user.is_authenticated}')
            else:
                return render(request, "register/register_error.html")
            return redirect("/home")
        else:
            #print(form)
            return redirect("/register")
    else:
        form = RegisterForm()
    return render(request, 'register/register.html', {"form":form})