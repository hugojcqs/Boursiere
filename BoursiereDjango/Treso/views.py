from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Beer.models import Beer, History
from Beer import models
# Create your views here.

def _calculate_income():
    total = 0
    total_buy_price = 0
    beer_sold = 0
    for hist in History.objects.all():
        total += hist.total_price
        total_buy_price += hist.buy_total_price
    return total, total_buy_price, total - total_buy_price

@login_required
def dashboard(request):
    total, total_buy_price, benef = _calculate_income()
    return render(request, 'dashboard.html', {'total':total, 'total_buy_price':total_buy_price, 'benef':benef, 'beers':Beer.objects.all()})
