from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from auth_user_app.models import User
from user_profile_app.models import User_education
from .serializers import SerachUserSerializer
from rest_framework.pagination import PageNumberPagination
from user_profile_app.serializers import UserProfileViewSerializer
from .serializers import UserConnectionRequestSendSerializer
from .models import UserConnectionRequestSend
class GetAllusersSetPagination(PageNumberPagination):
    page_size = 20
    # page_size_query_param = 'users'
    max_page_size = 10000

class GetAllUserPaginationView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SerachUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = GetAllusersSetPagination


class GetSpecificUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, userid):
        try:
            return User.objects.get(userid=userid)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, userid, format=None):
        user = self.get_object(userid)
        serializer = UserProfileViewSerializer(user)
        return Response(serializer.data)



class ConnectionRequestSendView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = UserConnectionRequestSend.objects.all()
    serializer_class= UserConnectionRequestSendSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserConnectionRequestSendSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)

















