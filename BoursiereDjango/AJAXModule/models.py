from django.db import models


class Timer(models.Model):
    timer_is_started = models.BigIntegerField(null=False)
    timer_start_time = models.BigIntegerField(null=False)
    timer_last_updated = models.BigIntegerField(null=False)
    timer_time_delay = models.IntegerField(default=15000)
