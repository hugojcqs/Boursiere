from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Beer.models import Beer, History, Timer, TresoFailsafe
import json
from datetime import datetime
import random
import string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib import messages


#--- NOT VIEWS PYTHON's FUNCTION

def _calculate_price(json_):
    total = 0
    for beer in json_:
        beer_db = Beer.objects.get(beer_name=beer)
        if beer_db is None:
            return -1
        total += beer_db.price * json_[beer]
    return round(total, 1)

def _random_string(string_length=10):
    letters = "123456789"
    return ''.join(random.choice(letters) for i in range(string_length))

def _calculate_time_to_next_update():
    timer = Timer.objects.get(id=1)
    if not timer.timer_is_started:
        return 0
    else:
        time_delta = timer.next_update - datetime.timestamp(datetime.now())
        return time_delta

#--- AJAX REQUEST VIEWS

@login_required
def calculate_price(request):
    if request.method == 'POST':
        json_ = request.POST.get('data')
        converted_json = json.loads(json_)
        return JsonResponse({'statut': 'ok', 'price': _calculate_price(converted_json)})
    return JsonResponse({'statut': 'ko'})


@login_required
def generate_data_set(request):
    labels = []
    prices = []
    for hist in History.objects.all():
        labels.append(hist.id)
        prices.append(hist.total_price)
    return JsonResponse(json.dumps({
      "labels": labels,
      "datasets": [
        {
          "label": "Revenu en euro",
          "backgroundColor": ["#3e95cd"],
          "data": prices
        }]}), safe=False)


@login_required
def make_order(request):
    if request.method == 'POST':
        json_ = json.loads(request.POST.get('data'))
        item_str = ''
        total = 0
        total_buy_price = 0
        time = datetime.now().strftime('%H:%M:%S')
        token = _random_string(10)

        for beer in json_:
            nb_beer = json_[beer]
            beer_db = Beer.objects.get(beer_name=beer)
            if beer_db is not None:
                beer_db.q_current_qarder += nb_beer
                beer_db.stock -= nb_beer
                total += beer_db.price * nb_beer
                total_buy_price += beer_db.buy_price * nb_beer
                item_str += '%d %s - ' % (nb_beer, beer)
                beer_db.save()

        item_str = item_str[0:len(item_str)-2]  # remove the last '-' from the string

        h = History.objects.create()
        h.id_str = token
        h.time = time
        h.total_price = round(total, 1)
        h.buy_total_price = round(total_buy_price, 1)
        h.history_json = request.POST.get('data')
        h.text = item_str
        h.save()

        return JsonResponse({'statut': 'ok', 'time': time, 'token': token, 'text': item_str, 'total_price': round(total, 1)})
    return JsonResponse({'statut': 'ko'})


def delete_histo(request):
    if request.method == 'POST':
        token = request.POST.get('data')
        hist = History.objects.get(id_str=token)
        if hist is None:
            return JsonResponse({'statut': 'ko', 'reason': 'History object not found!'})

        json_ = json.loads(hist.history_json)
        for beer in json_:
            beer_db = Beer.objects.get(beer_name=beer)
            if beer_db is None:
                return JsonResponse({'statut':'ko', 'reason':'The beer %s does not exist!' % beer})
            beer_db.stock += json_[beer]

            # SECURITY TO AVOID MISS IN PRICE COMPUTING
            #TODO: check if the id of qarder are the same...

            if(beer_db.q_qarder - json_[beer]) > 0:
                beer_db.q_qarder -= json_[beer]         # can be replace by beer_db.add_conso(-json_[beer]) (à tester)

            beer_db.save()
        hist.delete()

    return JsonResponse({'statut': 'ok'}, safe=False)


def activate_failsafe(request):
    #TODO: check permission du user..
    if request.method == 'POST':

        if request.user.groups.filter(name='admin').exists():

            if request.user.check_password(request.POST.get('data')):
                t = TresoFailsafe.objects.get(id=1)
                t.is_activated = True
                t.save()
                print('safe mode activated.')
                return JsonResponse({'statut':'ok'})

        else:
            print('error: access refused')
    return JsonResponse({'statut':'ko'})


def update_price_failsafe(request):

    if request.method == 'POST':
        timer = Timer.objects.get(id=1)
        timer.timer_is_started = True
        timer.next_update = (datetime.timestamp(datetime.now()) + 15 * 60 + 3)
        timer.save()
        tab = json.loads(request.POST.get('new_prices'))
        for id_, price in tab:
            beer = Beer.objects.get(beer_name = id_)
            beer.trend = Beer.get_trend(q_qarder=beer.q_qarder, q_current_qarder=beer.q_current_qarder)

            beer.q_qarder = beer.q_current_qarder  # q_current_qarder beer become last quarder consomaition
            beer.q_current_qarder = 0  # reset current qarder consomation

            if beer.stock <= 0:
                beer.out_of_stock = True

            beer.price = price
            beer.save()

    return JsonResponse({'statut':'ok'})


def timer_to_next_up(request):
    time_next_up_delta = _calculate_time_to_next_update()
    return JsonResponse({'statut':'ok', 'time_remaining':time_next_up_delta, 'pourcent':100 - (time_next_up_delta / (15 * 60)) * 100})


def update_stock(request):  # TODO : Passer le processus dans le model beer pour la creation du json
    #  TODO : Known bug - si une biere est ajouter sans mise a jour de la page de stock, celle ci ne sera pas afficher par l'ajax
    beers = {}

    beers['pourcent'] = 100 - (_calculate_time_to_next_update() / (15 * 60)) * 100

    for beer in Beer.objects.all():
        beer_name = beer.id
        beers[beer_name] = {}
        beers[beer_name]['price'] = beer.price
        beers[beer_name]['best_price'] = beer.best_price
        beers[beer_name]['best_value'] = beer.best_value
        beers[beer_name]['stock'] = beer.stock
        beers[beer_name]['trend'] = beer.trend
        beers[beer_name]['out_of_stock'] = beer.out_of_stock

    return JsonResponse({'statut': 'ok', 'data': beers})


@csrf_exempt
def update_price(request):

    TOKEN = 'CABB74F774DD3ACB'

    if request.method == 'POST':
        token = request.POST.get('token')
        if token == TOKEN:
           Beer._update_prices(do_round=True)
           return JsonResponse({'statut':'ok'})
    return JsonResponse({'statut':'ko'})


@csrf_exempt
def sound_ajax(request):
    t = Timer.objects.get(id=1)
    return JsonResponse({'statut':'ok', 'next_update':t.next_update})
