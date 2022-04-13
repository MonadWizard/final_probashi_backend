from dataclasses import dataclass
from django.db import connection, connections
from asgiref.sync import sync_to_async

from user_chat_app.models import ChatTable

from user_chat_app.db_utility import create_chat_table
from user_chat_app.db_utility import get_last_chat_data

@sync_to_async
def get_all_chat_data(userid):
    chat_list = ChatTable.objects.using('probashi_chat').filter(user_1=userid).order_by('-id')

    # if 
    # data = chat_list
    print(chat_list)
    data = {}
    for chat in chat_list:
        print(chat.user_2)
        data[chat.user_2] = get_last_chat_data(chat.user_1, chat.user_2)
    
    # print(data)

    # data = {
    #     'demo4': [
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'}
    #     ],
    #     'jahid-hasan': [
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'}
    #     ],
    #     'rakib-hasn': [
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'},
    #         {'sender': 'demo2', 'receiver': 'demo4', 'message': 'hi', 'time': '2020-01-01'}
    #     ]
    # }
    
    return data

@sync_to_async
def save_chat_data(data):
    try:    
        chat_table = ChatTable.objects.using('probashi_chat').get(user_1=data['sender'], user_2=data['receiver'])
        print('table-found')
    except:
        table_title = create_chat_table(user_1=data['sender'], user_2=data['receiver'])
        chat_table = ChatTable.objects.using('probashi_chat').create(user_1=data['sender'], user_2=data['receiver'], table_name=table_title)
        chat_table = ChatTable.objects.using('probashi_chat').create(user_1=data['receiver'], user_2=data['sender'], table_name=table_title)
        print('create-a-table')

    sql = "INSERT INTO " + str(chat_table.table_name) + "("
    
    index = 1
    for key in data.keys():
        sql += str(key)
        
        if index != len(data.keys()):
            sql += ','
        
        index += 1
    
    sql += ") VALUES ("
    
    index = 1
    for value in data.values():
        if type(value) == str:
                value = value.replace("'", "''")

        sql += "'" + str(value) + "'"        

        if index != len(data.values()):
            sql += ','
        
        index += 1

    sql += ")"

    try:
        with connections['probashi_chat'].cursor() as cursor:
            cursor.execute(sql)

            return True
    except Exception as e:
        print(e)
        print('error')
        return False

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

