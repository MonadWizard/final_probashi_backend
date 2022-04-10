# from db.connection import Connection
from dataclasses import dataclass
from django.db import connection
from asgiref.sync import sync_to_async

@sync_to_async
def get_all_chat_data(userid):
    # userid = current user
    # data's users are associated with the userid
    data = {
        'demo4': [
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'}
        ],
        'jahid-hasan': [
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'}
        ],
        'rakib-hasn': [
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'}
        ]
    }
    
    return data

@sync_to_async
def get_previous_chat_data(userid, associated_user_id, page):
    data = {
        'demo4': [
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
            {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'}
        ]
    }
    
    return data