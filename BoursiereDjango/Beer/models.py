from django.db import models
import datetime

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

    def __str__(self):
        return self.beer_name
    #  TODO : Validateur pour la verification des données


class History(models.Model):
    id_str = models.CharField(max_length=25, null=False)
    time = models.CharField(null=False, max_length=25)
    total_price = models.FloatField(null=False, default=0)
    history_json = models.TextField()  # to save data as json
    text = models.TextField(null=False, default="")
