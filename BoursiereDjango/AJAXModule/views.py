from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.
import json
@login_required
def calculate_price(request):
    if request.method == 'POST':
        json_ = request.POST.get('json_')
        converted_json = json.load(json_)
        for beer in converted_json:
            print(beer)
    return JsonResponse({'statut': 'ok', 'price':''})