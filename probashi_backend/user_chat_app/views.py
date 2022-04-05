from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from rest_framework.decorators import api_view
from django.db import connection




@api_view(["GET"])
def CreateFriendsMathcTable(request):

    with connection.cursor() as cursor:

        try:
            create_friendmatchtable = f"""CREATE SEQUENCE friendmatchtable_id_seq;
                    CREATE TABLE IF NOT EXISTS public.friendmatchtable (
                    id bigint NOT NULL DEFAULT nextval('friendmatchtable_id_seq'::regclass),


                    CONSTRAINT friendmatchtable_pkey PRIMARY KEY (id)
                    )
                    TABLESPACE pg_default;

                    ALTER TABLE IF EXISTS public.friendmatchtable
                        OWNER to postgres;
                    """

            cursor.execute(create_friendmatchtable)
                

            for i in range(1,1599):
                a = f'''
                        ALTER TABLE friendmatchtable
                        ADD COLUMN column_{i} text;'''
                cursor.execute(a)

                

            # query = s
            # print(s)
            # cursor.execute(query_from_json)
            # row = cursor.fetchall()
            # print(row)


            return Response(
                {
                    "status": "success",
                    "message": "Table created successfully",
                    "data": 'row',
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            err_msg = str(e)
            return Response(
                {
                    "status": "fail",
                    "message": err_msg,
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


    # return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def friendsMatchGenerate(request):
    # add_user_to_userMatch = 
    with connection.cursor() as cursor:

        try:

            return Response(
                    {
                        "status": "success",
                        "message": "Table created successfully",
                        "data": 'row',
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            err_msg = str(e)
            return Response(
                {
                    "status": "fail",
                    "message": err_msg,
                },
                status=status.HTTP_406_NOT_ACCEPTABLE,
            ) 




