import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

from user_chat_app.db_utilities_async import get_previous_chat_data
from user_chat_app.db_utilities_async import get_all_chat_data
from user_chat_app.db_utilities_async import save_chat_data, save_chat_data_image

class DemoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['userid']

        self.room_group_name = 'chat_' + self.room_name
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # get previous data
        data = await get_all_chat_data(self.room_name)
        # print('last message::::::::::::',data)
        data = dict(data)
        data_l = list(data.values())
        data_l = list(filter(None, data_l))
        print("data_l::::::::::::::::::::::::", data_l)

        await self.send(text_data=json.dumps({
            'success': True,
            'type': 'recent',
            'data': data_l,
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print('text_data_json::::::::::::',text_data_json)
        
        if text_data_json['data'] == 'reload_previous_chat':
            data = await get_previous_chat_data(userid=self.room_name, associated_user_id=text_data_json['associated_user_id'], chat_id=text_data_json['chat_id'])
            chat_data = data
        
        elif text_data_json['data'] == 'text':
            data = {
                'sender': self.room_name,
                'receiver': text_data_json['receiverid'],
                'message': text_data_json['message'],
                'message_time': str(datetime.datetime.now(datetime.timezone.utc)),
                'is_text_message': True,
            }

            await save_chat_data(data=data)

            chat_data = {
                'type': 'single message',
                'sender': self.room_name,
                'receiver': text_data_json['receiverid'],
                'message': text_data_json['message'],
                # 'status': 'sent',
                'message_time': str(datetime.datetime.now(datetime.timezone.utc)),
                "message-type": text_data_json['data'],
            }           
        
            self.room_name_temp = text_data_json['receiverid']
            self.room_group_name_temp = 'chat_' + self.room_name_temp

            await self.channel_layer.group_send(self.room_group_name_temp,{
                'type': 'send_chat',
                # 'data': data,
                'data': chat_data,


            })



# images send.................................................

        
        elif text_data_json['data'] == 'image':
            data = {
                'sender': self.room_name,
                'receiver': text_data_json['receiverid'],
                'message': text_data_json['message'],
                'message_time': str(datetime.datetime.now(datetime.timezone.utc)),
                'is_image_message': True,
            }

            await save_chat_data_image(data=data)

            chat_data = {
                'type': 'single message',
                'sender': self.room_name,
                'receiver': text_data_json['receiverid'],
                'message': text_data_json['message'],
                # 'status': 'sent',
                'message_time': str(datetime.datetime.now(datetime.timezone.utc)),
                "message-type": text_data_json['data'],
            }           
        
            self.room_name_temp = text_data_json['receiverid']
            self.room_group_name_temp = 'chat_' + self.room_name_temp

            await self.channel_layer.group_send(self.room_group_name_temp,{
                'type': 'send_chat',
                # 'data': data,
                'data': chat_data,


            })
















        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_chat',
            'data': chat_data,
            # 'data': data,

        })     
        

    async def send_chat(self, event):
        data = event['data']
        await self.send(text_data=json.dumps({

            'data': data,
            
            
        }))












































# class DemoConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.sender = self.scope['url_route']['kwargs']['sender']
#         self.receiver = self.scope['url_route']['kwargs']['receiver']
#         self.room_name_sr = self.sender + '_' + self.receiver
#         self.room_name_rs = self.receiver + '_' + self.sender
#         self.get_roomnamedata_sr = await self.get_roomname_sr()
#         self.get_roomnamedata_rs = await self.get_roomname_rs()
        

#         if self.get_roomnamedata_sr == True:        
#             self.room_group_name =  'chat' + self.room_name_sr
#         elif self.get_roomnamedata_rs == True:
#             self.room_group_name =  'chat' + self.room_name_rs
#         else:
#             self.room_group_name = await self.create_roomname()
        
#         await self.channel_layer.group_add(self.room_group_name,self.channel_name)
#         await self.accept()


#         data = await self.get_previous_chat()

#         await self.send(text_data=json.dumps({
#             'success': True,
#             'data': data,
#         }))



#     @database_sync_to_async
#     def get_previous_chat(self):

#         with connections['probashi_chat'].cursor() as cursor:
#             a = f'''
#                     SELECT * FROM {self.room_group_name}
#                     ORDER BY id DESC LIMIT 30
#                 '''

#             cursor.execute(a)
#             result = cursor.fetchall()
#             chat =[]
#             c = {}
#             for row in result:
#                 # c["id:"] = row[0]
#                 c["message:"] = row[1]
#                 c["date_time:"] = str(row[2])
#                 c["userid:"] = row[3]
#                 # print(c)
#                 chat.append(c.copy())

#         return chat


#     @database_sync_to_async
#     def get_roomname_sr(self):
#         get_roomname = RoomGroupNameTable.objects.using('probashi_chat').filter(Q(user_1=self.sender) & Q(user_2=self.receiver)).exists() 
#         return (get_roomname)

#     @database_sync_to_async
#     def get_roomname_rs(self):
#         get_roomname = RoomGroupNameTable.objects.using('probashi_chat').filter(Q(user_1=self.receiver) & Q(user_2=self.sender)).exists() 
#         return (get_roomname)

#     @database_sync_to_async
#     def create_roomname(self):
#         new_room_group_name = 'chat' + self.sender + '_' + self.receiver

#         RoomGroupNameTable.objects.create(user_1=self.sender, user_2=self.receiver, room_group_name = new_room_group_name)

#         with connections['probashi_chat'].cursor() as cursor:
#                 a = f'''
#                         CREATE SEQUENCE {new_room_group_name}_id_seq;
#                         CREATE TABLE IF NOT EXISTS {new_room_group_name}
#                     (
#                         id bigint NOT NULL DEFAULT nextval('{new_room_group_name}_id_seq'::regclass),
#                         message text COLLATE pg_catalog."default" NOT NULL,
#                         date_time timestamp with time zone NOT NULL,
#                         userid character varying(20) COLLATE pg_catalog."default" NOT NULL,
#                         CONSTRAINT {new_room_group_name}_pkey PRIMARY KEY (id)
#                     )

#                     TABLESPACE pg_default;

#                     ALTER TABLE IF EXISTS {new_room_group_name}
#                         OWNER to agl;
#                     '''

#                 cursor.execute(a)

#         return (new_room_group_name)





#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name,self.channel_name)



#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)

#         if text_data_json['data'] == 'resend':
#             self.page = text_data_json['page']
#             '''
#             {"data":"resend","page":"2"}
#             '''
#             data = await self.paginate_previous_chat()
#             chat_data = data
#         else:
#             user = self.sender
#             date_time = str(datetime.datetime.now())
#             data = {
#                 "chat": 
#                     {"user": user,"message": text_data_json['data'],"date_time": date_time}
#                 }
            
#             chat_data = 'message-sent'
        
#             self.room_name_temp = self.receiver + '_' + self.sender
#             self.room_group_name_temp = self.room_group_name

#             self.getdata = data
#             self.get_data_func = await self.get_data()

#             await self.channel_layer.group_send(self.room_group_name_temp,{
#                 'type': 'send_chat',
#                 'data': data,
#             })
#         await self.channel_layer.group_send(self.room_group_name, {
#             'type': 'send_chat',
#             'data': chat_data,
#         })


#     @database_sync_to_async
#     def paginate_previous_chat(self):
        
#         limit = 30
#         offset = (int(self.page) - 1) * limit

#         with connections['probashi_chat'].cursor() as cursor:
#             a = f'''
#                     SELECT * FROM {self.room_group_name}
#                     ORDER BY id DESC LIMIT {limit}
#                     OFFSET {offset}

#                 '''

#             cursor.execute(a)
#             result = cursor.fetchall()
#             chat =[]
#             c = {}
#             for row in result:
#                 # c["id:"] = row[0]
#                 c["message:"] = row[1]
#                 c["date_time:"] = str(row[2])
#                 c["userid:"] = row[3]
#                 chat.append(c.copy())

#         return chat
        


#     @database_sync_to_async
#     def get_data(self):
#         userid = self.getdata['chat']['user']
#         message = self.getdata['chat']['message']
#         date_time = self.getdata['chat']['date_time']



#         with connections['probashi_chat'].cursor() as cursor:
#                 a = f'''
#                         INSERT INTO {self.room_group_name}(
# 	                    message, date_time, userid)
# 	                    VALUES ( '{message}', '{date_time}', '{userid}');
#                     '''

#                 cursor.execute(a)

#         # return (d)
        
        

#     async def send_chat(self, event):
#         data = event['data']

#         await self.send(text_data=json.dumps({
#             'data': data,
            
#         }))





'''
basic message sending:

    {"data": "kisui kori na vai... hudai boisa asi."}


pagination message sending:
    {"data":"resend","page":"2"}

'''