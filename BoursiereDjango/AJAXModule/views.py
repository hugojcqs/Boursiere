from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Beer.models import Beer

# Create your views here.
import json
@login_required
def calculate_price(request):
    if request.method == 'POST':
        json_ = request.POST.get('json_')
        converted_json = json.loads(json_)
        total = 0
        for beer in converted_json:
            beer_db = Beer.objects.get(beer_name=beer)
            total += beer_db.price * converted_json[beer]
        return JsonResponse({'statut': 'ok', 'price':total})
    return JsonResponse({'statut': 'ko'})
