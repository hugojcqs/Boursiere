from django.contrib import admin
from .models import Beer as BeerModel
from .models import History as HistoryModel
# Register your models here.
admin.site.register(BeerModel)
admin.site.register(HistoryModel)
