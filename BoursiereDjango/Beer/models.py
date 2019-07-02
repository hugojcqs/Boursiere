from django.db import models

# Create your models here.
class Beer(models.Model):
    beer_name = models.CharField(max_length=100)
    price = models.FloatField(null=False)
    buy_price = models.FloatField(null=False)
    stock = models.IntegerField(null=False)
    coef_up = models.FloatField(null=False)
    coef_down = models.FloatField(null=False)
    coef_max = models.FloatField(null=False)
    q_qarder = models.IntegerField(null=False)
    q_current_qarder = models.IntegerField(null=False)
    small_image = models.ImageField()
    large_image = models.ImageField()

    #  TODO : Validateur pour la verification des données