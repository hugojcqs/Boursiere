from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from django.core import serializers


class WSNotifier:
    @staticmethod
    def notify_change_in_stock(id_pk, stock):
        message = {'action': 'update_qtt', 'id': id_pk, 'qtt': stock}

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'display',
            {
                'type': 'websocket.send',
                'text': json.dumps(message)
            }
        )

    @staticmethod
    def notify_next_update(next_update):
        message = {'action': 'time', 'next_update': next_update}

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'time',
            {
                'type': 'websocket.send',
                'text': json.dumps(message)
            }
        )

    @staticmethod
    def notify_price_update(beers, best_price_ids, best_beer_id):
        beers = serializers.serialize('json', beers)

        message = {'action': 'update_price', 'beers': beers, 'best_prices':best_price_ids, 'best_beer':best_beer_id}

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'display',
            {
                'type': 'websocket.send',
                'text': json.dumps(message)
            }
        )

    @staticmethod
    def notify_sound():
        message = {'action': 'play_sound'}

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'sound',
            {
                'type': 'websocket.send',
                'text': json.dumps(message)
            }
        )