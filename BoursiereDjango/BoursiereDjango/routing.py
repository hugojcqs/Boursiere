from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.conf.urls import url
from sms.consumers import *
from sms.consumers_display import *

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
           URLRouter(
               [
                    url("feed", MessageControlConsumer),
                    url("display", MessageDisplayConsumer),
               ]
           )
        )
    )
})