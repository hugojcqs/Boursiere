from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Beer.models import Beer
import json


@login_required
def calculate_price(request):
    if request.method == 'POST':
        json_ = request.POST.get('data')
        converted_json = json.loads(json_)
        return JsonResponse({'statut': 'ok', 'price':_calculate_price(converted_json)})
    return JsonResponse({'statut': 'ko'})


def _calculate_price(json_):
    total = 0
    for beer in json_:
        beer_db = Beer.objects.get(beer_name=beer)
        total += beer_db.price * json_[beer]
    return total

@login_required
def make_order(request):
    pass