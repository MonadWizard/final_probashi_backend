from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import (
    GoogleSocialAuthSerializer,
    FacebookSocialAuthSerializer,
    LinkedinSocialAuthSerializer,
    AppleSocialAuthSerializer
)

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
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer
    renderer_classes = [UserRenderer]

    #       POST with "auth_token" Send an access token as from facebook to get user information
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)


class LinkedinSocialAuthView(GenericAPIView):

    serializer_class = LinkedinSocialAuthSerializer
    renderer_classes = [UserRenderer]

    #       POST with "auth_token" Send an access token as from facebook to get user information
    def post(self, request):
        # print("request.data:::",request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        return Response(data, status=status.HTTP_200_OK)


class AppleSocialAuthView(GenericAPIView):

    serializer_class = AppleSocialAuthSerializer
    # renderer_classes = [UserRenderer] 

    def post(self, request):
        # data = request.data["auth_token"]
        # print("request.data:::", request.data["auth_token"])

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = (serializer.validated_data)["auth_token"]
        data["user_callphone"] = None

        print(data)
        return Response(data, status=status.HTTP_200_OK)