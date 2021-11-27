from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserEntryForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User
from django.contrib import messages
from flight.models import Booked


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 1:
                    return redirect('admin')
                else:
                    return redirect('index')
            else:
                messages.info(request, 'Username Password not matched')
                return redirect(request.path)

    return render(request, 'login.html')


def user_reg(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = UserEntryForm()
        if request.method == 'POST':
            form = UserEntryForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('login'))
    return render(request, 'regipage.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def admin(request):
    booked = Booked.objects.all()
    return render(request, 'admin.html', {'booked': booked})


def info(request):
    return render(request, 'info.html')
