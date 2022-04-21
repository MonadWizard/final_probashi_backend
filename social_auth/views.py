from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer, LinkedinSocialAuthSerializer

# from .serializers import GoogleSocialAuthSerializer, TwitterAuthSerializer, FacebookSocialAuthSerializer
from probashi_backend.renderers import UserRenderer
from auth_user_app.models import User
from django.http import Http404
from auth_user_app.utils import Util

class GoogleSocialAuthView(GenericAPIView):
    # renderer_classes = [UserRenderer]

    serializer_class = GoogleSocialAuthSerializer

        # POST with "auth_token" Send an idtoken as from google to get user information
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer
    renderer_classes = [UserRenderer]


#       POST with "auth_token" Send an access token as from facebook to get user information
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)



class LinkedinSocialAuthView(GenericAPIView):

    serializer_class = LinkedinSocialAuthSerializer
    renderer_classes = [UserRenderer]


#       POST with "auth_token" Send an access token as from facebook to get user information
    def post(self, request):
        # print("request.data:::",request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)



# class CompleteRegistrationSocialAuth(GenericAPIView):
#     renderer_classes = [UserRenderer]

#     # def get_object(self,user_email):
#     #     try:
#     #         return User.objects.get(user_email__exact=user_email)
#     #     except User.DoesNotExist:
#     #         raise Http404

#     # def get(self,request,user_email):
#     #     user_email = self.get_object(user_email)
#     #     serializer = UpdateRegisterSerializer(user_email)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)


#     def put(self,request):
#         # print('request.data:', request.data)
#         # user_email = self.get_object(user_email)
#         user_id = request.user.userid
#         print('user_id:::::::', user_id)
#         # request.data['user_fullname'] =request.data['user_fullname_passport']
#         # del request.data['user_fullname_passport']
#         # fullname_pasport = request.data['user_fullname']
#         # serializer = UpdateRegisterSerializer(user_email,data=request.data)
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         # user_data = serializer.data

#         # userid = User.objects.filter(user_email=user_email.user_email).values('userid')[0]['userid']
#         # # print('userid::::::::::::', userid)
#         # # call friend match table asynchronously
#         # # asyncio.run(match_friends(userid))
#         # # friend match call sync..........................................................
#         # # match_friends(user_id=userid)
        
#         # # relativeLink = reverse('email-verify')
#         # email_body = 'Hi '+fullname_pasport + \
#         #     ' welcome to probashi.. \n'
#         # data = {'email_body': email_body, 'to_email': user_email,
#         #         'email_subject': 'welcome to probashi'}
#         # # print('data:::::::::', data)

#         # Util.send_email(data)
#         return Response('user_data', status=status.HTTP_200_OK)
    
















