from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # path('chat/<str:sender>/<str:receiver>/', consumers.DemoConsumer.as_asgi()),
    path('chat/<str:userid>/', consumers.DemoConsumer.as_asgi()),
]





# response body = 
# {
#   'data' : {
#     "message": "Hello, world!",
#     "senderid": 124545456454
#      }
# }     











#  ws://127.0.0.1:8000/chat/2/3

# basic message sending:

#     {"data": "kisui kori na vai... hudai boisa asi."}


# pagination message sending:
#     {"data":"resend","page":"2"}
