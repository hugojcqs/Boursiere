from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.conf.urls import url
from Beer.consumers_display import *
from Beer.consumers_sound import *
from Beer.consumers_time import *
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
           URLRouter(
               [
                    url("display", MessageDisplayConsumer),
                    url("sound", MessageSoundConsumer),
                    url("time", MessageTimeConsumer),
               ]
           )
        )
    )
})