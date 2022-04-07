import datetime
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import RoomGroupNameTable
from django.db.models import Q
from channels.db import database_sync_to_async
from django.db import connections
# import asyncio


class DemoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['url_route']['kwargs']['sender']
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        self.room_name_sr = self.sender + '_' + self.receiver
        self.room_name_rs = self.receiver + '_' + self.sender
        self.get_roomnamedata_sr = await self.get_roomname_sr()
        self.get_roomnamedata_rs = await self.get_roomname_rs()
        

        if self.get_roomnamedata_sr == True:        
            self.room_group_name =  'chat' + self.room_name_sr
        elif self.get_roomnamedata_rs == True:
            self.room_group_name =  'chat' + self.room_name_rs
        else:
            self.room_group_name = await self.create_roomname()
        
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()


        # --------------get data from table-----------------

        # data = [
        #     {'user':'Shaon','message': 'hello', 'date_time': '2020-01-01 16:00:00'},
        #     {'user':'Rakib','message': 'Hi, how are you?', 'date_time': '2020-01-01 16:00:00'},
        #     {'user':'Shaon','message': 'Im am fine', 'date_time': '2020-01-01 16:00:00'},  
        #     {'user':'Shaon','message': 'How are you?', 'date_time': '2020-01-01 16:00:00'},  
        #     {'user':'Shaon','message': '*I am', 'date_time': '2020-01-01 16:00:00'},
        # ]
        # ws://base-url/demo/sender-user-id/receiver-user-id/

        data = await self.get_previous_chat()

        await self.send(text_data=json.dumps({
            'success': True,
            'data': data,
        }))



    @database_sync_to_async
    def get_previous_chat(self):

        with connections['probashi_chat'].cursor() as cursor:
            a = f'''
                    SELECT * FROM {self.room_group_name}
                    ORDER BY id DESC LIMIT 30
                '''

            cursor.execute(a)
            result = cursor.fetchall()
            chat ={}
            for row in result:
                chat["id:"] = row[0]
                chat["message:"] = row[1]
                chat["date_time:"] = str(row[2])
                chat["userid:"] = row[3]
                
            # print('chat: ', chat)
        return chat


    @database_sync_to_async
    def get_roomname_sr(self):
        get_roomname = RoomGroupNameTable.objects.using('probashi_chat').filter(Q(user_1=self.sender) & Q(user_2=self.receiver)).exists() 
        print('get_roomname_sr: ', get_roomname)
        return (get_roomname)

    @database_sync_to_async
    def get_roomname_rs(self):
        get_roomname = RoomGroupNameTable.objects.using('probashi_chat').filter(Q(user_1=self.receiver) & Q(user_2=self.sender)).exists() 
        print('get_roomname_rs: ', get_roomname)
        return (get_roomname)

    @database_sync_to_async
    def create_roomname(self):
        new_room_group_name = 'chat' + self.sender + '_' + self.receiver
        print(type(new_room_group_name), new_room_group_name)
        # new_room_group_name = 'table_name1'

        RoomGroupNameTable.objects.create(user_1=self.sender, user_2=self.receiver, room_group_name = new_room_group_name)

        with connections['probashi_chat'].cursor() as cursor:
                a = f'''
                        CREATE SEQUENCE {new_room_group_name}_id_seq;
                        CREATE TABLE IF NOT EXISTS public.{new_room_group_name}
                        (
                            id bigint NOT NULL DEFAULT nextval('{new_room_group_name}_id_seq'::regclass),
                            message text COLLATE pg_catalog."default" NOT NULL,
                            date_time timestamp with time zone NOT NULL,
                            userid character varying(20) COLLATE pg_catalog."default" NOT NULL,
                            CONSTRAINT {new_room_group_name}_pkey PRIMARY KEY (id)
                        )

                        TABLESPACE pg_default;

                        ALTER TABLE IF EXISTS public.{new_room_group_name}
                            OWNER to agl;

                        CREATE INDEX IF NOT EXISTS {new_room_group_name}_userid_6d510b74
                            ON public.{new_room_group_name} USING btree
                            (userid COLLATE pg_catalog."default" ASC NULLS LAST)
                            TABLESPACE pg_default;
                        
                        CREATE INDEX IF NOT EXISTS {new_room_group_name}_userid_6d510b74_like
                            ON public.{new_room_group_name} USING btree
                            (userid COLLATE pg_catalog."default" varchar_pattern_ops ASC NULLS LAST)
                            TABLESPACE pg_default;
                    '''

                cursor.execute(a)

        # print('create_roomname: ', new_room_group_name)
        return (new_room_group_name)





    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)



    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json['data'] == 'resend':
            page = text_data_json['page']
            # print('page: ', page)
            '''
            {"data":"resend","page":"2"}
            '''

            # an async function will be called
            # which will actually behave like pagination
            data_user1 = {
                "message_1": {'user':'Shaon','message': 'hello', 'date_time': '2020-01-01 16:00:00'},
                "message_2": {'user':'Rakib','message': 'Hi, how are you?', 'date_time': '2020-01-01 16:00:00'},
            }
        else:
            user = self.sender
            date_time = str(datetime.datetime.now())
            data = {
                "chat": 
                    {"user": user,"message": text_data_json['data'],"date_time": date_time}
                }
            
            data_user1 = 'message-sent'
        
            self.room_name_temp = self.receiver + '_' + self.sender
            self.room_group_name_temp = self.room_group_name

            print('room_name_temp: ' + self.room_group_name_temp)

            # print('data: ', data)
# --------------------------------------------------------------------
            self.getdata = data
            self.get_data_func = await self.get_data()

            await self.channel_layer.group_send(self.room_group_name_temp,{
                'type': 'send_demo_data',
                'data': data,
            })
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'send_demo_data',
            'data': data_user1,
        })


    @database_sync_to_async
    def get_data(self):
        # print('data:::::::::::: ', self.getdata['chat'])
        userid = self.getdata['chat']['user']
        message = self.getdata['chat']['message']
        date_time = self.getdata['chat']['date_time']


        # print('userid: ', userid, 'message: ', message, 'date_time: ', date_time)

        with connections['probashi_chat'].cursor() as cursor:
                a = f'''
                        INSERT INTO {self.room_group_name}(
	                    message, date_time, userid)
	                    VALUES ( '{message}', '{date_time}', '{userid}');
                    '''

                cursor.execute(a)

        # return (d)
        
        

    async def send_demo_data(self, event):
        data = event['data']
        # print('event data:::: ', data)

        await self.send(text_data=json.dumps({
            'data': data,
            
        }))


