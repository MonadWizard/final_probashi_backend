import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from django.db.models import Q
from user_setting_other_app.models import Notification
from auth_user_app.models import User
from asgiref.sync import sync_to_async


from user_chat_app.db_utilities_async import get_previous_chat_data
from user_chat_app.db_utilities_async import (
    get_all_chat_data,
    get_all_notifications,
    ChatOnlineUsers,
    OnlineStatusSend,
    OnlineStatusSend_connection,
    OnlineStatusSend_others,
)
from user_chat_app.db_utilities_async import (
    save_chat_data,
    save_chat_data_image,
    save_notification_data,
    delete_notification_data,
    seen_notification_data,
    OnlineStatusSend_self,
)
from django.utils import timezone

import base64
from pathlib import Path
import os

from django.conf import settings
from user_connection_app.utility import match_friends

all_online_user = []


class DemoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.connect_user = self.scope["url_route"]["kwargs"]["userid"]
        # self.room_name = self.scope["url_route"]["kwargs"]["userid"]
        self.room_name = ""
        if '-background' in self.connect_user:
            self.room_name = self.connect_user.split("-")[0]
            # self.room_name = self.scope["url_route"]["kwargs"]["userid"]
            self.room_group_name = "chat_" + self.room_name

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            # get previous data
            limit = 1
            data = await get_all_chat_data(self.room_name, limit)
            data = dict(data)
            data_l = list(data.values())
            data_l = list(filter(None, data_l))
            noti_data = await get_all_notifications(self.room_name)

            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "type": "recent",
                        "chat": data_l,
                        "notification": noti_data,
                    }
                )
            )


        else:
            self.room_name = self.connect_user
            self.room_group_name = "chat_" + self.room_name

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            all_online_user.append(self.room_name)
            await OnlineStatusSend_self(self.room_name, all_online_user)
            await OnlineStatusSend_others(self.room_name, all_online_user)

            # get previous data
            limit = 1
            data = await get_all_chat_data(self.room_name, limit)
            data = dict(data)
            data_l = list(data.values())
            data_l = list(filter(None, data_l))
            noti_data = await get_all_notifications(self.room_name)

            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "type": "recent",
                        "chat": data_l,
                        "notification": noti_data,
                    }
                )
            )

    async def disconnect(self, close_code):

        if '-background' not in self.connect_user:
            all_online_user.remove(self.room_name)
            await OnlineStatusSend(self.room_name, all_online_user)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        chat_data = {}
        text_data_json = json.loads(text_data)

        if text_data_json["data"] == "friend_match":
            userid = self.room_name
            await match_friends(user_id=userid)

        elif text_data_json["data"] == "paginate_recent_chat":
            userid = self.room_name
            limit = int(text_data_json["page"])
            data = await get_all_chat_data(userid, limit)
            data = dict(data)
            data_l = list(data.values())
            data_l = list(filter(None, data_l))
            await self.send(
                text_data=json.dumps(
                    {
                        "success": True,
                        "type": "all_recent",
                        "chat": data_l,
                    }
                )
            )

        elif text_data_json["data"] == "reload_previous_chat":
            data = await get_previous_chat_data(
                userid=self.room_name,
                associated_user_id=text_data_json["associated_user_id"],
                chat_id=text_data_json["chat_id"],
            )
            chat_data = data

        elif text_data_json["data"] == "text":
            timee = timezone.localtime(timezone.now())
            data = {
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "message": text_data_json["message"],
                "message_time": str(timee),
                "is_text_message": True,
            }

            table_status = await save_chat_data(data=data)
            self.room_name_temp = text_data_json["receiverid"]
            self.room_group_name_temp = "chat_" + self.room_name_temp
            # exist       new
            if table_status == "new":
                userid = self.room_name_temp
                limit = 1
                data = await get_all_chat_data(userid, limit)
                data = dict(data)
                data_l = list(data.values())
                data_l = list(filter(None, data_l))
                recent_data = {
                    "type": "latest_recent",
                    "chat": data_l,
                }

                # chat_data = recent_data
                await self.channel_layer.group_send(
                    self.room_group_name_temp,
                    {
                        "type": "send_chat",
                        # 'data': data,
                        "data": recent_data,
                    },
                )

                self.room_group_name_2 = "chat_" + self.room_name
                userid = self.room_name
                limit = 1
                data = await get_all_chat_data(userid, limit)
                data = dict(data)
                data_l = list(data.values())
                data_l = list(filter(None, data_l))
                recent_data = {
                    "type": "latest_recent",
                    "chat": data_l,
                }

                await self.channel_layer.group_send(
                    self.room_group_name_2,
                    {
                        "type": "send_chat",
                        # 'data': data,
                        "data": recent_data,
                    },
                )

            chat_data = {
                "type": "single message",
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "message": text_data_json["message"],
                "message_time": str(timee),
                "message-type": text_data_json["data"],
            }

            await self.channel_layer.group_send(
                self.room_group_name_temp,
                {
                    "type": "send_chat",
                    "data": chat_data,
                },
            )

        # images send.................................................
        elif text_data_json["data"] == "image":
            timee = timezone.localtime(timezone.now())

            image_data_byte = str.encode(text_data_json["message"])
            image_media_root = settings.MEDIA_ROOT
            image_save_dir = f"{image_media_root}/ChatAppData/images"
            if not os.path.exists(image_save_dir):
                try:
                    Path(f"{image_save_dir}").mkdir(parents=True, exist_ok=True)
                    print("directory created")
                except:
                    print("can not build dir")

            current_time = datetime.datetime.now()
            current_time = current_time.strftime("%m%d%H%M%S%f")
            image_name = current_time + text_data_json["extention"]
            image_save_path = f"{image_save_dir}/{image_name}"

            try:
                with open(f"{image_save_path}", "wb") as new_file:
                    new_file.write(base64.decodebytes(image_data_byte))
            except Exception as e:
                print("can not save image", e)
            data = {
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "message": image_save_path,
                "message_time": str(timee),
                "is_image_message": True,
            }
            table_status = await save_chat_data_image(data=data)
            # recent chat............................................................
            self.room_name_temp = text_data_json["receiverid"]
            self.room_group_name_temp = "chat_" + self.room_name_temp
            # exist       new
            if table_status == "new":
                userid = self.room_name_temp
                limit = 1
                data = await get_all_chat_data(userid, limit)
                data = dict(data)
                data_l = list(data.values())
                data_l = list(filter(None, data_l))
                recent_data = {
                    "type": "latest_recent",
                    "chat": data_l,
                }
                # chat_data = recent_data
                await self.channel_layer.group_send(
                    self.room_group_name_temp,
                    {
                        "type": "send_chat",
                        "data": recent_data,
                    },
                )

                self.room_group_name_2 = "chat_" + self.room_name
                userid = self.room_name
                limit = 1
                data = await get_all_chat_data(userid, limit)
                data = dict(data)
                data_l = list(data.values())
                data_l = list(filter(None, data_l))
                recent_data = {
                    "type": "latest_recent",
                    "chat": data_l,
                }

                await self.channel_layer.group_send(
                    self.room_group_name_2,
                    {
                        "type": "send_chat",
                        # 'data': data,
                        "data": recent_data,
                    },
                )

            chat_data = {
                "type": "single message",
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "message": image_save_path,
                # 'status': 'sent',
                "message_time": str(timee),
                "message-type": text_data_json["data"],
            }
            self.room_name_temp = text_data_json["receiverid"]
            self.room_group_name_temp = "chat_" + self.room_name_temp

            await self.channel_layer.group_send(
                self.room_group_name_temp,
                {
                    "type": "send_chat",
                    # 'data': data,
                    "data": chat_data,
                },
            )

        # get all notification.................................................
        elif text_data_json["data"] == "get-notification":
            noti_data = await get_all_notifications(self.room_name)
            chat_data = {
                "type": "notification-list",
                "data": noti_data,
            }

            self.room_name_temp = text_data_json["receiverid"]
            self.room_group_name_temp = "chat_" + self.room_name_temp
            await self.channel_layer.group_send(
                self.room_group_name_temp,
                {
                    "type": "send_chat",
                    # 'data': data,
                    "data": chat_data,
                },
            )

        # notification send.................................................
        elif text_data_json["data"] == "post-notification":
            data = {
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "notification_title": text_data_json["notification_title"],
                "notification_description": text_data_json["notification_description"],
                "notification_date": str(timezone.localtime(timezone.now())),
            }
            # Save to DataBase.................
            await save_notification_data(noti_data=data)
            chat_data = {
                "type": "notification",
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "notification_title": text_data_json["notification_title"],
                "notification_description": text_data_json["notification_description"],
                "notification_date": str(timezone.localtime(timezone.now())),
                "is_notification_delete": False,
                "is_notification_seen": False,
            }
            self.room_name_temp = text_data_json["receiverid"]
            self.room_group_name_temp = "chat_" + self.room_name_temp
            await self.channel_layer.group_send(
                self.room_group_name_temp,
                {
                    "type": "send_chat",
                    # 'data': data,
                    "data": chat_data,
                },
            )

        # delete notification data ....................................
        elif text_data_json["data"] == "delete-notification":
            data = {
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "notification_id": text_data_json["notification_id"],
                "is_notification_delete": text_data_json["is_notification_delete"],
            }

            # update to DataBase.................
            noti_time = await delete_notification_data(noti_data=data)
            chat_data = {
                "type": "notification",
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "notification_id": text_data_json["notification_id"],
                "is_notification_delete": text_data_json["is_notification_delete"],
                "notification_date": str(noti_time),
            }
            self.room_name_temp = text_data_json["receiverid"]
            self.room_group_name_temp = "chat_" + self.room_name_temp
            await self.channel_layer.group_send(
                self.room_group_name_temp,
                {
                    "type": "send_chat",
                    # 'data': data,
                    "data": chat_data,
                },
            )

        # notification seen.................................................
        elif text_data_json["data"] == "seen-notification":
            # print('delete notification::::::::::::',text_data_json)
            data = {
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "notification_id": text_data_json["notification_id"],
                "is_notification_seen": text_data_json["is_notification_seen"],
            }
            # update to DataBase.................
            noti_time = await seen_notification_data(noti_data=data)
            chat_data = {
                "type": "notification",
                "sender": self.room_name,
                "receiver": text_data_json["receiverid"],
                "notification_id": text_data_json["notification_id"],
                "is_notification_seen": text_data_json["is_notification_seen"],
                "notification_date": str(noti_time),
            }

            self.room_name_temp = text_data_json["receiverid"]
            self.room_group_name_temp = "chat_" + self.room_name_temp

            await self.channel_layer.group_send(
                self.room_group_name_temp,
                {
                    "type": "send_chat",
                    # 'data': data,
                    "data": chat_data,
                },
            )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_chat",
                "data": chat_data,
                # 'data': data,
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
