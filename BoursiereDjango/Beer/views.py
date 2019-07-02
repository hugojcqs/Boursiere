from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BeerForm
# Create your views here.
from django.contrib import messages


def beer_ordering_view(request):
    return render(request, 'ordering_beer_page.html')


def add_beer(request):
    beer_form = BeerForm()
    if beer_form.is_valid():
        pass  # TODO add beer to the database and process the image.
    return render(request, 'add_beer.html', {'form':beer_form})


def root(request):
    return redirect('beer_ordering')