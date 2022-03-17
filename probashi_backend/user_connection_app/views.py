from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.http import Http404
from auth_user_app.models import User
from .serializers import SerachUserSerializer
from rest_framework.pagination import PageNumberPagination
from user_profile_app.serializers import UserProfileViewSerializer
from .serializers import (UserFavouriteRequestSendSerializer, UserFavouriteRequestsSerializer,
                        AcceptFavouriteRequestSerializer,RejectFavouriteRequestSerializer)
from .models import UserFavoutireRequestSend, UserFavouriteList
from django.db.models import Q

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


class FavouriteRequestSendView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = UserFavoutireRequestSend.objects.all()
    serializer_class= UserFavouriteRequestSendSerializer

    def create(self, request):
        user = self.request.user
        user_id = User.objects.filter(user_email=user).values('userid')
        user_id = user_id[0].get('userid')
        if request.data['userid'] == user_id:
            if UserFavoutireRequestSend.objects.filter(Q(userid__exact=user_id) & Q(favourite_request_to__exact=request.data['favourite_request_to'])).exists():
                return Response('You can not send request to same user', status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = UserFavouriteRequestSendSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('serializer.errors', status=status.HTTP_400_BAD_REQUEST)



class FavouriteRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class= UserFavouriteRequestsSerializer

    def get_queryset(self):
            user = self.request.user
            return UserFavoutireRequestSend.objects.filter(Q(favourite_request_to=user) & Q(is_favourite_accept=False) & Q(is_favourite_reject=False))
    
    def list(self, request, format=None):
        queryset = self.get_queryset()
        serializer = UserFavouriteRequestsSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)  



class AcceptFavouriteRequest(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self,requestid):
        try:
            return UserFavoutireRequestSend.objects.get(id=requestid)
        except UserFavoutireRequestSend.DoesNotExist:
            raise Http404

    def put(self,request,requestid):

        user = self.request.user
        if UserFavoutireRequestSend.objects.filter(Q(favourite_request_to__exact=user.userid) & Q(id__exact=requestid) & Q(is_favourite_accept=False)).exists():    

            requested_data = self.get_object(requestid)
            follow_acceptuser= requested_data.favourite_request_to
            # follow_acceptuser_id = requested_data.favourite_request_to.userid
            follow_requesteduser= requested_data.userid
            # follow_requesteduser_id = requested_data.userid.userid
            print('accepted::::',follow_acceptuser, ",requested::::",follow_requesteduser)

            serializer = AcceptFavouriteRequestSerializer(requested_data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                UserFavouriteList.objects.create(userid=follow_acceptuser,favourite_userid=follow_requesteduser)
                UserFavoutireRequestSend.objects.filter(Q(userid__exact=follow_acceptuser) & Q(favourite_request_to__exact=follow_requesteduser)).update(is_favourite_accept=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)



class RejectFavouriteRequest(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self,requestid):
        try:
            return UserFavoutireRequestSend.objects.get(id=requestid)
        except UserFavoutireRequestSend.DoesNotExist:
            raise Http404

    def put(self,request,requestid):
        user = self.request.user
        if UserFavoutireRequestSend.objects.filter(Q(favourite_request_to__exact=user.userid) & Q(id__exact=requestid)& Q(is_favourite_reject=False)).exists():    
            requested_data = self.get_object(requestid)
            serializer = RejectFavouriteRequestSerializer(requested_data, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)












