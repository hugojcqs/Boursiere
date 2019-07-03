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
    return render(request, 'ordering_beer_page.html')

@login_required
def add_beer(request):
    beer_form = BeerForm()
    if request.method == 'POST':  # TODO : Verify form validation here
        beer_form = BeerForm(request.POST)
    if beer_form.is_valid():
        print('VALID')
        beer = BeerModel.objects.create()
        beer.beer_name = beer_form.cleaned_data['beer_name']
        beer.price = beer_form.cleaned_data['price']
        beer.buy_price = beer_form.cleaned_data['price']
        beer.coef_down = beer_form.cleaned_data['coef_down']
        beer.coef_up = beer_form.cleaned_data['coef_up']
        beer.coef_max = beer_form.cleaned_data['coef_max']
        beer.image = ImageUtilities.resize_save_image(beer_form.cleaned_data['image'].data.read(), 100, 100)
        beer.save()

    return render(request, 'add_beer.html', {'form':beer_form})


def root(request):
    return redirect('beer_ordering')


def login_page(request):
    login_form = LoginForm()
    if request.method == 'POST':  # TODO : Verify form validation here
        login_form = LoginForm(request.POST)
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