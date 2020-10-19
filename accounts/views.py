
from .forms import UserRegisterForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from django.contrib import messages


from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from django.shortcuts import redirect

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('phone')
            raw_password = form.cleaned_data.get('password1')


            user = authenticate(username=username, password=raw_password)
            if user is not None:
                auth_login(request, user,backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})




def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "accounts/login.html",
                    context={"form":form})

def logout(request):
    auth_logout(request)
    messages.info(request, "Logged out successfully!")
    return render(request,'/')
