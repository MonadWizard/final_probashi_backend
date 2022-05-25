from datetime import datetime
from django.db import connection, connections
from auth_user_app.models import User
from .utility import sql_array_to_object

from user_chat_app.models import ChatTable


def create_chat_table(user_1, user_2):
    table_title = (
        "chat_"
        + user_1
        + "_"
        + user_2
        + "_"
        + str(datetime.now().strftime("%Y%m%d%H%M%S"))
    )

    sql = "CREATE TABLE " + str(table_title) + "("
    sql += "id SERIAL PRIMARY KEY,"
    sql += "sender VARCHAR(255) NOT NULL,"
    sql += "receiver VARCHAR(255) NOT NULL,"
    sql += "is_text_message BOOLEAN NOT NULL DEFAULT FALSE,"
    sql += "is_file_message BOOLEAN NOT NULL DEFAULT FALSE,"
    sql += "is_audio_message BOOLEAN NOT NULL DEFAULT FALSE,"
    sql += "is_image_message BOOLEAN NOT NULL DEFAULT FALSE,"
    sql += "message TEXT NOT NULL,"
    sql += "message_time TIMESTAMP WITH TIME ZONE DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'Asia/Dhaka')"
    sql += ")"

    # timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
    # print(sql)

    with connections["probashi_chat"].cursor() as cursor:
        cursor.execute(sql)

    return table_title


def get_last_chat_data(user_1, user_2, table_namee):
    table_title = (
        ChatTable.objects.using("probashi_chat")
        .get(user_1=user_1, user_2=user_2)
        .table_name
    )

    sql = (
        "SELECT id,receiver,sender,message,is_text_message,is_file_message,is_audio_message,is_image_message,message_time AT TIME ZONE 'Asia/Dhaka' FROM "
        + str(table_title)
        + " ORDER BY id DESC LIMIT 1"
    )

    # print('sql::::get last chat data::::::::',sql)

    with connections["probashi_chat"].cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchone()

        # print('result::::::', result)

        if result is None:
            return {}

    # print('result::::::', result)

    fields = [field[0] for field in cursor.description]

    # print('fields::::::', fields)

    result = sql_array_to_object(values=result, field_names=fields)
    result["message_time"] = str(result["timezone"]) + str("+06:00")
    del result["id"]
    result["id"] = table_namee
    del result["timezone"]
    try:
        # print('sender::::::',result['sender'])
        sender_data = User.objects.filter(userid=result["sender"]).values(
            "userid", "user_fullname", "is_consultant", "user_photopath"
        )[0]

        # online_sender = User.objects.get(userid=sender_data["userid"]).is_online
        # sender_data["is_online"] = online_sender
        result["sender"] = sender_data

        receiver_data = User.objects.filter(userid=result["receiver"]).values(
            "userid", "user_fullname", "is_consultant", "user_photopath"
        )[0]

        # online_reciver = User.objects.get(userid=receiver_data["userid"]).is_online
        # receiver_data["is_online"] = online_reciver
        result["receiver"] = receiver_data

        return result

    except Exception as e:
        print(e)
        return {}
