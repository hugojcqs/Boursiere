from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Beer.models import Beer
import json
from datetime import datetime
import random
import string

@login_required
def calculate_price(request):
    if request.method == 'POST':
        json_ = request.POST.get('data')
        converted_json = json.loads(json_)
        return JsonResponse({'statut': 'ok', 'price': _calculate_price(converted_json)})
    return JsonResponse({'statut': 'ko'})


def _calculate_price(json_):
    total = 0
    for beer in json_:
        beer_db = Beer.objects.get(beer_name=beer)
        total += beer_db.price * json_[beer]
    return total


def _random_string(string_length=10):
    letters = "123456789"
    return ''.join(random.choice(letters) for i in range(string_length))


@login_required
def make_order(request):
    if request.method == 'POST':
        json_ = json.loads(request.POST.get('data'))
        item_str = ''
        total = 0
        time = datetime.now().strftime('%H:%M:%S')
        token = _random_string(10)
        
        for beer in json_:
            nb_beer = json_[beer]
            beer_db = Beer.objects.get(beer_name=beer)
            beer_db.q_current_qarder += nb_beer
            beer_db.stock -= nb_beer
            total += beer_db.price * nb_beer
            item_str += '%d %s -' % (nb_beer, beer)
            beer_db.save()
        item_str = item_str[0:len(item_str)-1]
        return JsonResponse({'statut': 'ok', 'time': time, 'token': token, 'text': item_str, 'total_price': total})
    return JsonResponse({'statut': 'ko'})

