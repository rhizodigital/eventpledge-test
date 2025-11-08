from django.urls import re_path
from .consumers import LiveCountsConsumer

websocket_urlpatterns = [
    re_path(r'^ws/live/$', LiveCountsConsumer.as_asgi()),
]
