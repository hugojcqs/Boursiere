import base64
import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core import serializers
from django.core.management.base import BaseCommand
from Beer.models import Beer, TresoFailsafe, Timer
import emoji
import datetime
from .ws_notifier import *
import time
from django.http import JsonResponse


class Command(BaseCommand):
    def handle(self, *args, **options):
        WSNotifier.notify_next_update(time.time() + 60)

