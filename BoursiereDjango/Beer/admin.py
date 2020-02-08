from django.contrib import admin
from .models import Beer as BeerModel
from .models import History as HistoryModel
from .models import Timer as TimerModel
from .models import Settings
# Register your models here.
admin.site.register(BeerModel)
admin.site.register(HistoryModel)
admin.site.register(TimerModel)
admin.site.register(Settings)
