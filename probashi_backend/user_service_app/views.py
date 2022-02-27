from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404




class DemoView(generics.GenericAPIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):

        return Response("user_service_app_view",status=status.HTTP_204_NO_CONTENT)





