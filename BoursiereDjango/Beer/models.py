from django.db import models
from django.db.models import *
from datetime import datetime


class Beer(models.Model):
    beer_name = models.CharField(max_length=100)
    price = models.FloatField(null=False)
    buy_price = models.FloatField(null=False)
    stock = models.IntegerField(null=False)
    coef_up = models.FloatField(null=False)
    coef_down = models.FloatField(null=False)
    coef_max = models.FloatField(null=False)
    q_qarder = models.IntegerField(null=False, default=0)
    q_current_qarder = models.IntegerField(null=False, default=0)
    alcohol_percentage = models.FloatField(null=False, default=0)
    bar = models.IntegerField(null=False, default=1)
    trend = models.CharField(max_length=10, default='EQUAL')
    out_of_stock = models.BooleanField(null=False, default=False)

    def change_percentage_alchohol(self, percentage):
        self.alcohol_percentage = percentage

    def change_coef_down(self, coef_down):
        self.coef_down = coef_down

    def change_coef_up(self, coef_up):
        self.coef_up = coef_up

    def change_coef_max(self, coef_max):
        self.coef_max = coef_max

    def add_conso(self, number):
        self.q_current_qarder += number

    def compute_price(self):
        if self.q_current_qarder > self.q_qarder:
            return self.price + self.coef_up * (self.q_current_qarder - self.q_qarder)
        else:
            return self.price + self.coef_down * (self.q_current_qarder - self.q_qarder)

    def change_stock(self, number):
        self.stock -= number


    @staticmethod
    def _stop_timer():
        timer = Timer.objects.get(id=1)
        timer.timer_is_started = False
        timer.next_update = (datetime.timestamp(datetime.now()) + 15 * 60 + 3)
        timer.save()


    @staticmethod
    def _update_prices(do_round=True):

        timer = Timer.objects.get(id=1)
        timer.timer_is_started = True
        timer.next_update = (datetime.timestamp(datetime.now()) + 15*60 + 3)
        timer.save()


        out_stock = []
        for beer in Beer.objects.all(): # for each beer
            new_price = beer.compute_price()

            beer.trend = Beer.get_trend(q_qarder=beer.q_qarder, q_current_qarder=beer.q_current_qarder)

            #beer.change_stock(beer.q_current_qarder)  # remove q_current_qarder from stock

            if beer.stock <= 0:
                out_stock.append(beer)      # add beer to out of stock beer list

            beer.q_qarder = beer.q_current_qarder #q_current_qarder beer become last quarder consomaition
            beer.q_current_qarder = 0              #reset current qarder consomation

            if new_price > (beer.coef_max * beer.buy_price):    #if new_price is too high , change it
                new_price = beer.coef_max * beer.buy_price

            if do_round:                               # if round is need
                beer.price = round(new_price, 1)       # round new price with 1 comma (roundup)
            else:
                beer.price = new_price
            beer.save()

        for out_beer in out_stock:   #for each beer out_of_stock
            # TODO: remove it from beer
            out_beer.out_of_stock = True
            out_beer.save()


    @staticmethod
    def get_trend(q_qarder, q_current_qarder):
        if q_current_qarder > q_qarder:
            return 'UP'
        elif q_current_qarder == q_qarder:
            return 'EQUAL'
        else:
            return 'DOWN'

    @staticmethod
    def get_worth_beers():
        worth_beers = Beer.objects.filter(price=Beer.objects.all().aggregate(Min('price'))['price__min'])  # get QuerySet with all minus price beers
        return worth_beers

    def __str__(self):
        return self.beer_name

    #  TODO : CHECK IF IT WORKS !!
    def verify_exist(self):
        beer = Beer.objects.get(self)
        if beer is None:
            raise Exception('Beer does not exists in the database')


class History(models.Model):
    id_str = models.CharField(max_length=25, null=False)
    time = models.CharField(null=False, max_length=25)
    total_price = models.FloatField(null=False, default=0)
    buy_total_price = models.FloatField(null=False, default=0)
    history_json = models.TextField()
    text = models.TextField(null=False, default="")


class Timer(models.Model):
    next_update = models.BigIntegerField(null=False)
    timer_is_started = models.BooleanField(null=False, default=False)


class TresoFailsafe(models.Model):
    is_activated = models.BooleanField(null=False, default=False)