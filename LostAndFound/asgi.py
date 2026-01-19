import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import findme.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LostAndFound.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            findme.routing.websocket_urlpatterns
        )
    ),
})
