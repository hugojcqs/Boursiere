from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Beer.models import Beer, History, Timer, TresoFailsafe
import json
from datetime import datetime
import random

"""
###########################################
Private function used by the (ajax) views
###########################################
"""


def _calculate_price(json_):
    """
    Responsible for calculating price of an order.
    :param json_: json from de javascript, containing the beer and the quantities associated with it.
    :return: total price based on database prices.
    """
    total = 0
    for beer in json_:
        beer_db = Beer.objects.get(beer_name=beer)
        if beer_db is None:
            return -1
        total += beer_db.price * json_[beer]
    return round(total, 1)

def _get_current_stock(json_):
    """
    Responsible for calculating price of an order.
    :param json_: json from de javascript, containing the beer and the quantities associated with it.
    :return: total price based on database prices.
    """

    dic=  {}
    for beer in json_:
        beer_db = Beer.objects.get(beer_name=beer)
        dic[beer] = beer_db.stock
    return json.dumps(dic)


def _random_string(string_length=10):
    """
    Responsible for generating random string
    :param string_length: generated string length
    :return: the random string
    """
    letters = "123456789"
    return ''.join(random.choice(letters) for i in range(string_length))


def _calculate_time_to_next_update():
    """
    Responsible for calculating time (in seconds) before the next update.
    :return: time remaining to the next update.
    """
    timer = Timer.objects.get(id=1)
    if not timer.timer_is_started:
        return -1
    else:
        time_delta = timer.next_update - datetime.timestamp(datetime.now())
        return time_delta


# --- AJAX REQUEST VIEWS
"""
###########################################
AJAX Views
###########################################
"""


@login_required
def calculate_price(request):
    """
    AJAX responsible for calculating the price of an order.
    :param request: request from the client.
    :return: JsonResponse
    """
    if request.method == 'POST':
        json_ = request.POST.get('data')
        converted_json = json.loads(json_)
        return JsonResponse({'status': True, 'price': _calculate_price(converted_json), 'now_stock': _get_current_stock(converted_json)})
    return JsonResponse(status=520, data={'status': False})


@login_required
def make_order(request):
    """
    AJAX responsible for adding an order to the database.
    :param request: request from the client.
    :return: JsonResponse
    """
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
                beer_db.out_of_stock = beer_db.stock <= 0         # set out_of_stock  beer when stock less than 0
                total += beer_db.price * nb_beer
                total_buy_price += beer_db.buy_price * nb_beer
                item_str += '%d %s - ' % (nb_beer, beer)
                beer_db.save()

        item_str = item_str[0:len(item_str) - 2]  # remove the last '-' from the string

        h = History.objects.create()
        h.id_str = token
        h.time = time
        h.quarter = Timer.objects.get(id=1).current_quarter
        h.total_price = round(total, 1)
        h.buy_total_price = round(total_buy_price, 1)
        h.history_json = request.POST.get('data')
        h.text = item_str
        h.save()

        return JsonResponse(
            {'status': True, 'time': time, 'token': token, 'text': item_str, 'total_price': round(total, 1)})

    return JsonResponse(status=404, data={'status': False, 'reason': 'Not yet defined'})


def delete_histo(request):
    """
    AJAX responsible for deleting a previous order. The quantities are restored to the remaining quantities.
    :param request: request from the client.
    :return: JsonResponse
    """
    if request.method == 'POST':
        token = request.POST.get('data')

        try:
            hist = History.objects.get(id_str=token)
        except:
            return JsonResponse(status=520, data={'status': False, 'reason': 'History object not found!'})

        json_ = json.loads(hist.history_json)
        for beer in json_:
            beer_db = Beer.objects.get(beer_name=beer)
            if beer_db is None:
                return JsonResponse(status=520, data={'status': False, 'reason': 'The beer %s does not exist!' % beer})
            beer_db.stock += json_[beer]
            if beer_db.stock > 0:
                beer_db.out_of_stock = False


            # SECURITY TO AVOID MISS IN PRICE COMPUTING
            # TODO: check if the id of qarder are the same...

            if (beer_db.q_qarder - json_[beer]) > 0:
                beer_db.q_qarder -= json_[beer]  # can be replace by beer_db.add_conso(-json_[beer]) (à tester)

            beer_db.save()
        hist.delete()

    return JsonResponse({'status': True}, safe=False)


def activate_failsafe(request):
    """
    AJAX Activate the failsafe and disable the update from the timer.
    :param request: request from the client.
    :return: JsonResponse
    """
    # TODO: check permission du user..
    # if request.method == 'POST':

    if request.user.groups.filter(name='admin').exists():

        if request.user.check_password(request.POST.get('data')):
            t = TresoFailsafe.objects.get(id=1)
            t.is_activated = True
            t.save()
            return JsonResponse({'status': True})
    return JsonResponse(status=404, data={'status': False, 'reason': 'Not yet defined'})


def update_price_failsafe(request):
    """
    AJAX Update price based on the price given by the trésoriers de mes balls.
    :param request: request from the client.
    :return: JsonResponse
    """
    if request.method == 'POST':
        timer = Timer.objects.get(id=1)
        timer.timer_is_started = True
        timer.next_update = (datetime.timestamp(datetime.now()) + 15 * 60 + 3)
        timer.save()
        tab = json.loads(request.POST.get('new_prices'))
        for id_, price in tab:
            beer = Beer.objects.get(beer_name=id_)
            beer.trend = Beer.get_trend(q_qarder=beer.q_qarder, q_current_qarder=beer.q_current_qarder)

            beer.q_qarder = beer.q_current_qarder  # q_current_qarder beer become last quarder consomaition
            beer.q_current_qarder = 0  # reset current qarder consomation

            if beer.stock <= 0:
                beer.out_of_stock = True

            beer.price = price
            beer.save()

    return JsonResponse({'status': True})


def timer_to_next_up(request):
    """
    AJAX responsible for giving the time to next update, the percent of progression to the next
    update and the current quarter.
    :param request: request from client.
    :return: JsonResponse
    """
    time_next_up_delta = _calculate_time_to_next_update()
    return JsonResponse({'status': True, 'time_remaining': time_next_up_delta,
                         'pourcent': 100 - (time_next_up_delta / (15 * 60)) * 100, 'quarter': Timer.objects.get(id=1).current_quarter})


def update_stock(request):
    """
    AJAX responsible for giving the dataset for updating the update_stock page table.
    :param request: request from client.
    :return: JsonResponse.
    """
    beers = {}

    beers['pourcent'] = 100 - (_calculate_time_to_next_update() / (15 * 60)) * 100

    for beer in Beer.objects.all():
        beer_name = beer.id
        beers[beer_name] = {}
        beers[beer_name]['price'] = beer.price
        beers[beer_name]['best_price'] = beer.best_price
        beers[beer_name]['best_value'] = beer.best_value
        beers[beer_name]['stock'] = beer.stock

        #test
        beers[beer_name]['stock_msg'] = beer.get_stock_left()


        beers[beer_name]['trend'] = beer.trend
        beers[beer_name]['out_of_stock'] = beer.out_of_stock

    return JsonResponse({'status': True, 'data': beers})
