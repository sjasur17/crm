from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.db.models.functions import Lower
from .models import Client
from .forms import ClientForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms

# Login forma
class LoginForm(forms.Form):
    username = forms.CharField(label='Foydalanuvchi nomi')
    password = forms.CharField(widget=forms.PasswordInput, label='Parol')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Login yoki parol noto‘g‘ri')
    else:
        form = LoginForm()
    return render(request, 'clients/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ro‘yxatdan o‘tish muvaffaqiyatli!')
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'clients/register.html', {'form': form})


@login_required
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'clients/logout_confirm.html')



# 📋 1. Mijozlar ro‘yxati
@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/client_list.html', {'clients': clients})


# ➕ 2. Yangi mijoz qo‘shish
# @login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'clients/client_form.html', {'form': form})


# ✏️ 3. Mijozni tahrirlash
@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/client_form.html', {'form': form})


# ❌ 4. Mijozni o‘chirish
@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'clients/client_confirm_delete.html', {'client': client})


# 📊 5. Dashboard statistikasi
@login_required
def dashboard(request):
    total_clients = Client.objects.count()
    domain_stats = (
        Client.objects
        .annotate(domain=Lower('email'))
        .values('domain')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    context = {
        'total_clients': total_clients,
        'domain_stats': domain_stats,
    }
    return render(request, 'clients/dashboard.html', context)
