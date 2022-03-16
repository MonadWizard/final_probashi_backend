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
from .serializers import (UserFavouriteRequestSendSerializer, UserFavouriteRequestsSerializer,
                        AcceptFavouriteRequestSerializer)
from .models import UserFavoutireRequestSend
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


class FavouriteRequestSendView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = UserFavoutireRequestSend.objects.all()
    serializer_class= UserFavouriteRequestSendSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserFavouriteRequestSendSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)



class FavouriteRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class= UserFavouriteRequestsSerializer

    def get_queryset(self):
            user = self.request.user
            return UserFavoutireRequestSend.objects.filter(favourite_request_to=user)
    
    def list(self, request, format=None):
        queryset = self.get_queryset()
        serializer = UserFavouriteRequestsSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)  



# class AcceptFavouriteRequest(generics.UpdateAPIView):
#     permission_classes = [permissions.IsAuthenticated,]
#     queryset = UserFavoutireRequestSend.objects.all()

#     serializer_class= AcceptFavouriteRequestSerializer



class AcceptFavouriteRequest(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self,requestid):
        try:
            return UserFavoutireRequestSend.objects.get(id=requestid)
        except UserFavoutireRequestSend.DoesNotExist:
            raise Http404

    def put(self,request,requestid):

        user = self.request.user
        if UserFavoutireRequestSend.objects.filter(userid__exact=user.userid) and UserFavoutireRequestSend.objects.filter(id__exact=requestid) :    

            requested_data = self.get_object(requestid)
            serializer = AcceptFavouriteRequestSerializer(requested_data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)














