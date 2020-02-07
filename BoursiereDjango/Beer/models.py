from django.db import models
from datetime import datetime
from django.db.models import Min, Max

class Beer(models.Model):
    beer_name = models.CharField(max_length=100)
    price = models.FloatField(null=False)
    buy_price = models.FloatField(null=False)
    stock = models.IntegerField(null=False)
    static_stock = models.IntegerField(null=False)
    coef_up = models.FloatField(null=False)
    coef_down = models.FloatField(null=False)
    coef_max = models.FloatField(null=False)
    coef_min = models.FloatField(null=False)
    q_qarder = models.IntegerField(null=False, default=0)
    q_current_qarder = models.IntegerField(null=False, default=0)
    alcohol_percentage = models.FloatField(null=False, default=0)
    bar = models.IntegerField(null=False, default=1)
    trend = models.CharField(max_length=10, default='EQUAL')
    out_of_stock = models.BooleanField(null=False, default=False)
    best_value = models.BooleanField(null=False, default=False)
    best_price = models.BooleanField(null=False, default=False)

    class Meta:
        permissions = (('show_tool_bar', 'Can show the toolbar'),
                       ('failsafe_mode', 'Can access to failsafe'),)

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
    def update_prices(do_round=True):

        Beer.reset_beers()

        # Moved timer modification to the
        timer = Timer.objects.get(id=1)
        timer.timer_is_started = True
        timer.current_quarter += 1
        timer.next_update = (datetime.timestamp(datetime.now()) + 15*60)
        timer.save()

        out_stock = []
        for beer in Beer.objects.all():  # for each beer
            new_price = beer.compute_price()

            beer.trend = Beer.get_trend(q_qarder=beer.q_qarder, q_current_qarder=beer.q_current_qarder)

            # beer.change_stock(beer.q_current_qarder)  # remove q_current_qarder from stock

            if beer.stock <= 0:
                out_stock.append(beer)      # add beer to out of stock beer list

            if 5 <= beer.stock <= 10:
                new_price = beer.buy_price * 2.1
            if beer.stock < 5:
                new_price = beer.buy_price * 2.5

            beer.q_qarder = beer.q_current_qarder  # q_current_qarder beer become last quarder consomaition
            beer.q_current_qarder = 0  # reset current qarder consomation

            # TO HIGH PRICE SECURITY

            if new_price > (beer.coef_max * beer.buy_price):  # if new_price is too high , change it
                new_price = beer.coef_max * beer.buy_price

            if new_price < (beer.coef_min * beer.buy_price): # if new_price is too lower, fix it.
                new_price = beer.coef_min * beer.buy_price

            # ROUND CHECK

            if do_round:                               # if round is need
                beer.price = round(new_price, 1)       # round new price with 1 comma (roundup)
            else:
                beer.price = new_price

            # SAVING EACH BEER OBJECT

            beer.save()
        Beer.set_best_value_beer()
        Beer.set_best_price()

        # SET BEER TO OUT OF STOCK

        for out_beer in out_stock:
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

    def get_stock_left(self):

        if self.stock <= 0:
            return 'plus de stock'
        elif self.stock <= round(self.static_stock/8):
            return 'quantité très faible'
        elif self.stock <= round(self.static_stock/4):
            return 'quantité faible'
        elif self.stock < round(self.static_stock/2) and self.stock > round(self.static_stock/4):
            return 'quantité affaiblie'
        else:
            return 'quantité suffisante'

    @staticmethod
    def reset_beers():
        for beer in Beer.objects.all():
            beer.best_price = False
            beer.best_value = False
            beer.save()

    @staticmethod
    def set_best_price():
        beers_min = Beer.objects.filter(price=Beer.objects.all().aggregate(Min('price'))['price__min'])
        print("Bière la moins chère : ", beers_min)
        for beer in beers_min:
            beer.best_price = True
            beer.save()

    @staticmethod
    def set_best_value_beer():
        max_price = Beer.objects.all().aggregate(Max('buy_price'))['buy_price__max']
        max_alcohol = Beer.objects.all().aggregate(Max('alcohol_percentage'))['alcohol_percentage__max']

        best_index = 1
        beer_index_list = []
        for beer in Beer.objects.all():
            index = beer.price / beer.alcohol_percentage
            if index <= best_index:
                best_index = index
                beer_index_list.append((index, beer))
            beer.save()

        beer = min(beer_index_list, key=lambda t: t[0])[1]
        beer.best_value = True
        beer.save()


    def __str__(self):
        return self.beer_name

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
    quarter = models.IntegerField(null=False, default=1)
    text = models.TextField(null=False, default="")


class Timer(models.Model):
    next_update = models.BigIntegerField(null=False)
    timer_is_started = models.BooleanField(null=False, default=False)
    current_quarter = models.IntegerField(null=False, default=1)


class TresoFailsafe(models.Model):
    is_activated = models.BooleanField(null=False, default=False)
