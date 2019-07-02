from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import BeerForm, LoginForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import messages

@login_required
def beer_ordering_view(request):
    return render(request, 'ordering_beer_page.html')

@login_required
def add_beer(request):
    beer_form = BeerForm()
    if beer_form.is_valid():
        beer_form.save()
        pass  # TODO add beer to the database and process the image.
    return render(request, 'add_beer.html', {'form':beer_form})


def root(request):
    return redirect('beer_ordering')


def login_page(request):
    print('Helooo1')

    login_form = LoginForm()
    if login_form.is_valid():
        login_form.save()
        print('Helooo54765')
        user = authenticate(request, username=login_form.username, password=login_form.password)
        if user is not None:
            login(request, user)
            redirect('beer_ordering')
        else:
            messages.add_message(request, messages.ERROR, 'Error during login!')
            print('Error in login')
            return render(request, 'login_page.html', {'form':login_form})
    return render(request, 'login_page.html', {'form':login_form})