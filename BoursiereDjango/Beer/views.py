from django.shortcuts import render, redirect
from django.http import Http404
from .forms import BeerForm
from .models import Beer as BeerModel
from .models import History
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
import random

# TODO V2: MAKE CLASS VIEW
# TODO: MAKE THIS THING BETTER CLEAR

# --- DEFAULT VIEWS


def root(request):
    return redirect('stock_page')


# --- BEER ORDERING VIEWS

@login_required
def beer_ordering_view(request):
    return render(request, 'ordering_beer_page.html', {'beers': BeerModel.objects.all(), 'history': History.objects.all()})

# --- STOCK VIEWS


@ensure_csrf_cookie  # generate CSRF token on stockpage
def stock_page(request):
    return render(request, 'stock_page.html', {'beers': BeerModel.objects.all()})

# --- BEER MANAGEMENT VIEWS


@login_required
def add_beer(request):
    beer_form = BeerForm()
    if request.method == 'POST':
        beer_form = BeerForm(request.POST, request.FILES)
    if beer_form.is_valid():
        # check if the beer is already saved.
        if beer_form.cleaned_data['beer_name'].upper() in [beer.beer_name.upper() for beer in BeerModel.objects.all()]:
            messages.add_message(request, messages.ERROR, 'Cette bière à déjà été enregistré !')
        else:
            BeerModel.objects.create(beer_name=beer_form.cleaned_data['beer_name'],
                                     price=beer_form.cleaned_data['price'],
                                     buy_price=beer_form.cleaned_data['price'],
                                     coef_down=beer_form.cleaned_data['coef_down'],
                                     coef_up=beer_form.cleaned_data['coef_up'],
                                     stock=beer_form.cleaned_data['stock'],
                                     static_stock=beer_form.cleaned_data['stock'],
                                     coef_max=beer_form.cleaned_data['coef_max'],
                                     coef_min=beer_form.cleaned_data['coef_min'],
                                     alcohol_percentage=beer_form.cleaned_data['alcohol_percentage'],
                                     bar=beer_form.cleaned_data['bar']
                                     )
            messages.add_message(request, messages.SUCCESS, 'La bière à bien été ajouté à la liste !')
    else:
        messages.error(request, beer_form.errors)
    return render(request, 'add_beer.html', {'form': beer_form})


@login_required
def delete_beer_page(request):
    return render(request, 'delete_beer.html', {'beers': BeerModel.objects.all()})


@login_required
def delete_beer(request, id_beer):

    try:
        BeerModel.objects.get(id=id_beer).delete()
    except Exception as e:
        print(e)
        raise Http404

    return redirect('delete_beer_page')

# --- ERROR VIEWS (need DEBUG=False in settings.py to works)


def error_404(request, exception):
    return render(request, '404.html', locals())


def error_500(request):
    return render(request, '500.html', locals())

# --- OTHER VIEWS


def sound_page(request):
    return render(request, 'sound_page.html')
