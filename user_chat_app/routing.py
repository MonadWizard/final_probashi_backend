from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('chat/<str:sender>/<str:receiver>/', consumers.DemoConsumer.as_asgi()),
    path("socket/<str:userid>/", consumers.DemoConsumer.as_asgi()),
]

