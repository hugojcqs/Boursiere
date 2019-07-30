from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from Beer.models import Beer, History, Timer, TresoFailsafe
from Beer import models
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
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
# @permission_required('Beer.failsafe_mode')
def dashboard(request):
    if request.user.has_perm('Beer.failsafe_mode'):
        total, total_buy_price, benef = _calculate_income()
        print(TresoFailsafe.objects.get(id=1).is_activated)
        return render(request,
                      'dashboard.html',
                      {'total': total,
                       'total_buy_price': total_buy_price,
                       'benef': benef, 'beers': Beer.objects.all(),
                       'failsafe': TresoFailsafe.objects.get(id=1).is_activated})
    else:
        # return HttpResponseForbidden()
        raise PermissionDenied()
