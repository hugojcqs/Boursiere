from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .forms import BeerForm, LoginForm
from .models import Beer as BeerModel
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib import messages
from .ImageUtilities import ImageUtilities
@login_required
def beer_ordering_view(request):
    beers = BeerModel.objects.all()
    return render(request, 'ordering_beer_page.html', {'beers':beers})

@login_required
def add_beer(request):

    beer_form = BeerForm()
    if request.method == 'POST':
        beer_form = BeerForm(request.POST, request.FILES )
    if beer_form.is_valid():
        #beer.image = ImageUtilities.resize_save_image(beer_form.cleaned_data['image'].read(), 100, 100)
        if beer_form.cleaned_data['beer_name'].upper() in [beer.beer_name.upper() for beer in BeerModel.objects.all()]: # check if the beer is already saved.
            messages.add_message(request, messages.ERROR, 'Cette bière à déjà été enregistré !')

        else:
            beer = BeerModel.objects.create(beer_name=beer_form.cleaned_data['beer_name'],
                                            price = beer_form.cleaned_data['price'],
                                            buy_price = beer_form.cleaned_data['price'],
                                            coef_down = beer_form.cleaned_data['coef_down'],
                                            coef_up = beer_form.cleaned_data['coef_up'],
                                            stock = beer_form.cleaned_data['stock'],
                                            coef_max = beer_form.cleaned_data['coef_max'])
            messages.add_message(request, messages.SUCCESS, 'La bière à bien été ajouté à la liste !')
    else:
        messages.error(request, beer_form.errors)
    return render(request, 'add_beer.html', {'form':beer_form})


def root(request):
    return redirect('beer_ordering')


def login_page(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user = authenticate(request, username=login_form.cleaned_data['username'], password=login_form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            return redirect('beer_ordering')
        else:
            messages.add_message(request, messages.ERROR, 'Login error!')
            return render(request, 'login_page.html', {'form':login_form})
    return render(request, 'login_page.html', {'form':login_form})


def logout_page(request):
    logout(request)
    return render(request, 'logout_page.html')
