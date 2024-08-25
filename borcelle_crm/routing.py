from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from celery_progress.websockets import routing
from notifications_app.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # Django's ASGI application to handle traditional HTTP requests
    "http": django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.urlpatterns +
            websocket_urlpatterns
        )
    ),
})
