from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
# Create your views here.


def logout_page(request):
    print('logout with success !!')
    logout(request)
    return redirect('login_page')


def login_page(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user = authenticate(request,
                            username=login_form.cleaned_data['username'],
                            password=login_form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect('stock_page')
        else:
            messages.add_message(request, messages.ERROR, 'Login error!')
            return render(request, 'login_page.html', {'form': login_form})
    return render(request, 'login_page.html', {'form': login_form})
