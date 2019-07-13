from django.db import models


class Timer(models.Model):
    timer_is_started = models.BigIntegerField(null=0)
    timer_start_time = models.BigIntegerField(null=0)
    timer_last_updated = models.BigIntegerField(null=0)
    timer_time_delay = models.IntegerField(null=15000)
