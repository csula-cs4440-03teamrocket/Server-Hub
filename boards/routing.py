from django.urls import re_path
from .consumers import WhiteboardConsumer

websocket_urlpatterns = [
    re_path(r'ws/whiteboard/$', WhiteboardConsumer.as_asgi()),
]