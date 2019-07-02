from django.shortcuts import render
from django.shortcuts import HttpResponse
from .forms import BeerForm
# Create your views here.
from django.contrib import messages

def beer_ordering_view(request):
    return render(request, 'ordering_beer_page.html')

def add_beer(request):
    beer_form = BeerForm()
    messages.add_message(request, messages.SUCCESS, 'Test')
    return render(request, 'add_beer.html', {'form':beer_form})