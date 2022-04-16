# from dataclasses import dataclass
from django.db import connection, connections
from asgiref.sync import sync_to_async
from probashi_backend.utility import sql_array_to_object

from user_chat_app.models import ChatTable

from user_chat_app.db_utility import create_chat_table
from user_chat_app.db_utility import get_last_chat_data

@sync_to_async
def get_all_chat_data(userid):
    chat_list = ChatTable.objects.using('probashi_chat').filter(user_1=userid).order_by('-id')
    data = {}

    for chat in chat_list:
        data[chat.user_2] = get_last_chat_data(chat.user_1, chat.user_2)
        # data['specific user'] = get_last_chat_data(chat.user_1, chat.user_2)

    
    print('::::::::::::', data)
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
    # off_set = 
    limit = 10 * int(page)
    offset = limit - 10
    data = {}

    try:
        chat_table = ChatTable.objects.using('probashi_chat').filter(user_1=userid, user_2=associated_user_id).order_by('-id')[0].table_name
        
        sql = "SELECT * FROM " + str(chat_table) + " ORDER BY id "
        sql += "OFFSET " + str(offset) + " ROWS "
        sql += "FETCH NEXT 10 ROWS ONLY"

        with connections['probashi_chat'].cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

            if result is None:
                return data

            fields = [field[0] for field in cursor.description]
            temp_data = []

            for row in result:
                d = sql_array_to_object(field_names=fields, values=row)
                d['message_time'] = str(d['message_time'])
                temp_data.append(d)
            
            # print('temp data::::::::',temp_data)
            #         
            # data[associated_user_id] = temp_data
            data['type'] = 'previous message'
            data['chat'] = temp_data
            
            
    except Exception as e:
        print(e)
        return data
    
    return data

