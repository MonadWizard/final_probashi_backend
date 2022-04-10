# from db.connection import Connection
from dataclasses import dataclass
from django.db import connection
from asgiref.sync import sync_to_async

@sync_to_async
def get_chat_data(userid, page):
    data = []
    
    return data