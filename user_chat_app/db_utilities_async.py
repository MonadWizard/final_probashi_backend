# from dataclasses import dataclass
from django.db import connection, connections
from asgiref.sync import sync_to_async
from pytz import timezone
from user_chat_app.utility import sql_array_to_object
from auth_user_app.utils import Util
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

from auth_user_app.models import User

from user_chat_app.models import ChatTable
from django.db.models import Q

from user_setting_other_app.models import Notification, User_settings

from user_chat_app.db_utility import create_chat_table
from user_chat_app.db_utility import get_last_chat_data
from itertools import chain
from datetime import datetime, timezone, timedelta
import pytz


@sync_to_async
def OnlineStatusSend_self(user_id, all_online_user):
    # all_online_user.append(user_id)
    chat_users = ChatOnlineUsers(user_id)
    # chat_users.append(user_id)

    # for i in chat_users:
    #     if i in self.all_online_user:
    #         online_chat_user.append(i)

    # self.online_chat_user.append(user_id)

    if chat_users:
        chat_users = list(chat_users)

        online_chat_user = []
        [online_chat_user.append(i) for i in chat_users if i in all_online_user]

        online_chat_user = list(set(online_chat_user))

        # print("online chat user self.........", online_chat_user)

        room_group_name = "chat_" + user_id

        async_to_sync(get_channel_layer().group_send)(
            room_group_name,
            {
                "type": "send_chat",
                "success": True,
                "data": {
                    "type": "online-users self",
                    "users": online_chat_user,
                },
            },
        )


@sync_to_async
def OnlineStatusSend_others(user_id, all_online_user):

    print("all_online_user.........", all_online_user)
    # all_online_user.append(user_id)
    chat_users = ChatOnlineUsers(user_id)

    # for i in chat_users:
    #     if i in self.all_online_user:
    #         online_chat_user.append(i)

    # self.online_chat_user.append(user_id)
    if chat_users:

        print("chat_users===================", chat_users)

        chat_users = list(chat_users)

        online_chat_user = []
        [online_chat_user.append(i) for i in chat_users if i in all_online_user]

        online_chat_user = list(set(online_chat_user))

        for user in online_chat_user:
            room_group_name = "chat_" + user

            async_to_sync(get_channel_layer().group_send)(
                room_group_name,
                {
                    "type": "send_chat",
                    "success": True,
                    "data": [
                        {
                            "type": "online-user",
                            "users": user_id,
                        }
                    ],
                },
            )














@sync_to_async
def OnlineStatusSend_connection(user_id, all_online_user):
    print("all_online_user connection===================", all_online_user)
    # all_online_user.append(user_id)
    chat_users = ChatOnlineUsers(user_id)

    if chat_users:

        print("chat_users===================", chat_users)

        chat_users = list(chat_users)

        online_chat_user = []
        [online_chat_user.append(i) for i in chat_users if i in all_online_user]

        online_chat_user.append(user_id)

        print("online chat user connection.........", online_chat_user)

        online_chat_user = list(set(online_chat_user))

        for user in online_chat_user:
            # if user != user_id:

            room_group_name = "chat_" + user

            async_to_sync(get_channel_layer().group_send)(
                room_group_name,
                {
                    "type": "send_chat",
                    "success": True,
                    "data": {
                        "type": "online-users",
                        "users": online_chat_user,
                    },
                },
            )


@sync_to_async
def OnlineStatusSend(user_id, all_online_user):

    print("all_online_user.........", all_online_user)
    # all_online_user.append(user_id)
    chat_users = ChatOnlineUsers(user_id)

    # for i in chat_users:
    #     if i in self.all_online_user:
    #         online_chat_user.append(i)

    # self.online_chat_user.append(user_id)
    if chat_users:

        print("chat_users===================", chat_users)

        chat_users = list(chat_users)

        online_chat_user = []
        [online_chat_user.append(i) for i in chat_users if i in all_online_user]

        online_chat_user = list(set(online_chat_user))

        for user in online_chat_user:
            room_group_name = "chat_" + user

            async_to_sync(get_channel_layer().group_send)(
                room_group_name,
                {
                    "type": "send_chat",
                    "success": True,
                    "data": [
                        {
                            "type": "offline-user",
                            "users": user_id,
                        }
                    ],
                },
            )


async def send_chat(self, event):
    data = event["data"]
    await self.send(
        text_data=json.dumps(
            {
                "data": data,
            }
        )
    )


def ChatOnlineUsers(user_id):
    try:
        if user1 := ChatTable.objects.filter(user_1=user_id).values_list(
            "user_2", flat=True
        ):
            return user1

    except Exception as e:
        print(e)
        return [user_id]


@sync_to_async
def update_online_true(user_id):
    User.objects.filter(userid=user_id).update(is_online=True)


@sync_to_async
def update_online_false(user_id):
    User.objects.filter(userid=user_id).update(is_online=False)


@sync_to_async
def get_all_chat_data(userid, limit):

    limit = limit or 1
    chat_list = (
        ChatTable.objects.using("probashi_chat")
        .filter(Q(user_1=userid) & ~Q(user_2=userid))
        .order_by("-id")[(limit - 1) * 20 : (limit * 20)]
    )
    data = {}
    # print("chat list:::::::::", chat_list)

    for chat in chat_list:
        data[chat.user_2] = get_last_chat_data(
            chat.user_1, chat.user_2, chat.table_name
        )

    return data


@sync_to_async
def save_chat_data(data):
    table_status = ""
    try:
        chat_table = ChatTable.objects.using("probashi_chat").get(
            user_1=data["sender"], user_2=data["receiver"]
        )

        table_status = "exist"
        print("table-found")
    except:
        table_title = create_chat_table(user_1=data["sender"], user_2=data["receiver"])
        chat_table = ChatTable.objects.using("probashi_chat").create(
            user_1=data["sender"], user_2=data["receiver"], table_name=table_title
        )
        chat_table = ChatTable.objects.using("probashi_chat").create(
            user_1=data["receiver"], user_2=data["sender"], table_name=table_title
        )
        table_status = "new"
        print("create-a-table")

    sql = "INSERT INTO " + str(chat_table.table_name) + "("

    index = 1
    for key in data.keys():
        sql += str(key)

        if index != len(data.keys()):
            sql += ","

        index += 1

    sql += ") VALUES ("

    index = 1
    for value in data.values():
        if type(value) == str:
            value = value.replace("'", "''")

        sql += "'" + str(value) + "'"

        if index != len(data.values()):
            sql += ","

        index += 1

    sql += ")"

    # print('::::::::::::::::sql', sql)

    try:
        with connections["probashi_chat"].cursor() as cursor:
            cursor.execute(sql)

            return table_status
    except Exception as e:
        # print(e)
        # print("error")
        return table_status


# image data save. ..............................................


@sync_to_async
def save_chat_data_image(data):
    table_status = ""
    try:
        chat_table = ChatTable.objects.using("probashi_chat").get(
            user_1=data["sender"], user_2=data["receiver"]
        )
        # print('table name::', chat_table.table_name)
        table_status = "exist"
        print("table-found....")
    except:
        table_title = create_chat_table(user_1=data["sender"], user_2=data["receiver"])
        chat_table = ChatTable.objects.using("probashi_chat").create(
            user_1=data["sender"], user_2=data["receiver"], table_name=table_title
        )
        chat_table = ChatTable.objects.using("probashi_chat").create(
            user_1=data["receiver"], user_2=data["sender"], table_name=table_title
        )
        table_status = "new"
        print("create-a-table")

    sql = "INSERT INTO " + str(chat_table.table_name) + "("

    index = 1
    for key in data.keys():
        sql += str(key)

        if index != len(data.keys()):
            sql += ","

        index += 1

    sql += ") VALUES ("

    index = 1
    for value in data.values():
        if type(value) == str:
            value = value.replace("'", "''")

        sql += "'" + str(value) + "'"

        if index != len(data.values()):
            sql += ","

        index += 1

    sql += ")"

    # print('sql:::::::::', sql)

    try:
        with connections["probashi_chat"].cursor() as cursor:
            cursor.execute(sql)
            return table_status
    except Exception as e:
        # print(e)
        # print('error')
        return table_status


@sync_to_async
def get_previous_chat_data(userid, associated_user_id, chat_id):
    # off_set =

    limit = int(chat_id)
    offset = limit - 10
    data = {}

    try:
        chat_table = (
            ChatTable.objects.using("probashi_chat")
            .filter(user_1=userid, user_2=associated_user_id)
            .order_by("-id")[0]
            .table_name
        )

        sql = (
            "SELECT id,receiver,sender,message,is_text_message,is_file_message,is_audio_message,is_image_message,message_time AT TIME ZONE 'Asia/Dhaka' FROM "
            + str(chat_table)
            + " ORDER BY id DESC "
        )
        sql += "OFFSET " + str(offset) + " ROWS "
        sql += "FETCH NEXT 10 ROWS ONLY "

        with connections["probashi_chat"].cursor() as cursor:
            # cursor.execute(f"SET timezone TO 'Asia/Dhaka'")
            cursor.execute(sql)
            result = cursor.fetchall()

            if result is None:
                return data

            fields = [field[0] for field in cursor.description]
            temp_data = []

            for row in result:
                d = sql_array_to_object(field_names=fields, values=row)
                d["message_time"] = str(d["timezone"]) + str("+06:00")
                del d["timezone"]
                temp_data.append(d)
                # print('d:::::::::', d)

            # print('temp_data:::::::::', temp_data)
            # data[associated_user_id] = temp_data
            data["type"] = "previous message"
            data["chat"] = temp_data

    except Exception as e:
        print("error", e)
        return data

    return data


# ===================================notification.................
@sync_to_async
def get_all_notifications(userid):
    # print('userid:::::::::', userid)
    tz = pytz.timezone("Asia/Dhaka")

    all_noti = (
        Notification.objects.filter(
            Q(receiverid=userid) & Q(is_notification_delete=False)
        )
        .order_by("is_notification_seen", "-id")
        .values()
    )

    for noti in all_noti:
        noti["notification_date"] = noti["notification_date"].replace(
            tzinfo=tz
        ) + timedelta(hours=6)

    noti_data = json.dumps(list(all_noti), sort_keys=True, default=str)

    noti_data_json = json.loads(noti_data)

    return noti_data_json


# =====================notification=================
@sync_to_async
def save_notification_data(noti_data):
    # print('noti-data:::::::::', noti_data)
    userid_data = User.objects.get(userid=noti_data["sender"])
    recever_data = User.objects.get(userid=noti_data["receiver"])
    try:
        Notification.objects.create(
            userid=userid_data,
            receiverid=recever_data,
            notification_title=noti_data["notification_title"],
            notification_description=noti_data["notification_description"],
            notification_date=noti_data["notification_date"],
            is_notification_seen=False,
            is_notification_delete=False,
        )
        print("noti-saved")

        if User_settings.objects.filter(
            Q(userid=recever_data.userid) & Q(user_mail_notification_enable=True)
        ).exists():
            user_fullname = recever_data.user_fullname
            user_email = recever_data.user_email
            noti_title = noti_data["notification_title"]
            email_body = f"""Hello,{user_fullname} \n You Have an notification about {noti_title}"""

            data = {
                "email_body": email_body,
                "to_email": user_email,
                "email_subject": "Probashi Notification",
            }

            Util.send_email(data)

        return True
    except Exception as e:
        print(e)
        return False


@sync_to_async
def delete_notification_data(noti_data):
    try:
        tz = pytz.timezone("Asia/Dhaka")
        # print('noti-data:::::::::', noti_data)
        noti_id = noti_data["notification_id"]
        delete_status = noti_data["is_notification_delete"]
        # print('noti-id:::::::::', noti_id, delete_status)
        Notification.objects.filter(id=noti_id).update(
            is_notification_delete=delete_status
        )

        time = Notification.objects.filter(id=noti_id).values("notification_date")
        # print('noti-time:::::::::', noti_time[0])
        # print('noti-time:::::::::', time[0]['notification_date'].replace(tzinfo=tz) + timedelta(hours=6))
        noti_time = time[0]["notification_date"].replace(tzinfo=tz) + timedelta(hours=6)
        return noti_time

    except Exception as e:
        print(e)
        return False


@sync_to_async
def seen_notification_data(noti_data):
    try:

        tz = pytz.timezone("Asia/Dhaka")
        # print('noti-data:::::::::', noti_data)
        noti_id = noti_data["notification_id"]
        seen_status = noti_data["is_notification_seen"]
        # print('noti-id:::::::::', noti_id, delete_status)
        Notification.objects.filter(id=noti_id).update(is_notification_seen=seen_status)

        time = Notification.objects.filter(id=noti_id).values("notification_date")
        noti_time = time[0]["notification_date"].replace(tzinfo=tz) + timedelta(hours=6)
        return noti_time

    except Exception as e:
        print(e)
        return False
