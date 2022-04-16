from multiprocessing import context
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from auth_user_app.models import User
from .serializers import SerachUserSerializer
from rest_framework.pagination import PageNumberPagination
from user_profile_app.serializers import UserProfileViewSerializer, UserProfileWithConsultancyViewSerializer
from .serializers import (UserFavouriteRequestSendSerializer, UserFavouriteRequestsSerializer,
                        AcceptFavouriteRequestSerializer,RejectFavouriteRequestSerializer,
                        UserFavouriteListSerializer)
from .models import UserFavoutireRequestSend, UserFavouriteList, FriendsSuggation
from django.db.models import Q
from itertools import chain
from django.db.models import F
import datetime
import json 
from rest_framework.pagination import PageNumberPagination


from user_connection_app.utility import match_friends


class TakeMatchFriend(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        # print('user:::::',user.userid)
        match_friends(user_id=user.userid)
        return Response(status=status.HTTP_200_OK)


# @api_view(['GET'])
# def take_match_friend(request):
#     # country
#     # city
#     # print("user", request.user)
#     print("::::::::::",request.user.userid)
#     permissions.IsAuthenticated.has_permission(request, request.user)
    

#     from user_connection_app.utility import match_friends



#     print(datetime.datetime.now())
#     match_friends(user_id="0409143135542106")
#     print(datetime.datetime.now())
#     match_friends(user_id="0409143232003081")
#     print(datetime.datetime.now())

#     return Response({
#         'message': 'Successfully matched friends'
#     })




class GetMatchFriendSetPagination(PageNumberPagination):
    page_size = 20
    # page_size_query_param = 'users'
    max_page_size = 10000

class Friends_suggation(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class= UserFavouriteRequestsSerializer
    pagination_class = GetMatchFriendSetPagination

    def get(self,request):
        user = request.user
        match_all = FriendsSuggation.objects.filter(user=user).values('location', 'goals', 'interest')[0]
        match_12 = FriendsSuggation.objects.filter(user=user).values('location', 'goals')[0]
        match_13 = FriendsSuggation.objects.filter(user=user).values('location', 'interest')[0]
        match_23 = FriendsSuggation.objects.filter(user=user).values('goals', 'interest')[0]

        match_friend_all = set.intersection(*[set(x) for x in match_all.values()])
        match_friend_12 = set.intersection(*[set(x) for x in match_12.values()])
        match_friend_13 = set.intersection(*[set(x) for x in match_13.values()])
        match_friend_23 = set.intersection(*[set(x) for x in match_23.values()])


        match_friend_id = set(chain(match_friend_all, match_friend_12, match_friend_13, match_friend_23))
        match_friend_data = []
        for mf in match_friend_id:
            match_friend = User.objects.filter(userid=mf).values('userid', 'user_fullname', 'user_areaof_experience', 'user_photopath', 'is_consultant')[0]
            match_friend_data.append(match_friend)
        
        data = {'data': match_friend_data}


        # paginator = self.pagination_class

        # # paginator.page_size = 10

        # # result_page = paginator.paginate_queryset(match_friend_id, request)

        # # serializer = TalentScoringSerializer(result_page, many=True)

        # return paginator.get_paginated_response(data)


        return Response(data)







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

    def get_object(self, user_id):
        try:
            return User.objects.get(userid=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        data = self.get_object(user_id)
        
        user = self.request.user
        if User.objects.filter(Q(is_consultant=False) & Q(userid=user.userid)).exists():
            serializer = UserProfileWithConsultancyViewSerializer(data)
            context = {'data': serializer.data}
            # print(context)
            return Response(context, status=status.HTTP_200_OK)
        
        elif User.objects.filter(Q(is_consultant=True) & Q(user_id=user.userid)).exists():
            serializer = UserProfileViewSerializer(data)
            context = {'data': serializer.data}
            # print(context)
            return Response(context, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


            
class FavouriteRequestSendView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = UserFavoutireRequestSend.objects.all()
    serializer_class= UserFavouriteRequestSendSerializer

    def create(self, request):
        user = self.request.user
        if request.data['userid'] == user.userid:
            if UserFavoutireRequestSend.objects.filter(Q(userid__exact=user.userid) & 
                                                    Q(favourite_request_to__exact=request.data['favourite_request_to'])).exists():
                return Response('You can not send request to same user', status=status.HTTP_400_BAD_REQUEST)
            
            if UserFavouriteList.objects.filter(Q(userid__exact=user.userid) & 
                                                Q(favourite_userid__exact=request.data['favourite_request_to'])).exists():
                return Response('You are Already Friend', status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer = UserFavouriteRequestSendSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)



class FavouriteRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class= UserFavouriteRequestsSerializer

    def get_queryset(self):
            user = self.request.user
            return UserFavoutireRequestSend.objects.filter(Q(favourite_request_to=user.userid) & 
                                                        Q(is_favourite_accept=False) & Q(is_favourite_reject=False))
    
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
        if request.data['is_favourite_accept'] == True:
            if UserFavoutireRequestSend.objects.filter(Q(favourite_request_to__exact=user.userid) & 
                                                    Q(id__exact=requestid) & Q(is_favourite_accept=False)).exists():    

                requested_data = self.get_object(requestid)
                follow_acceptuser= requested_data.favourite_request_to
                follow_requesteduser= requested_data.userid

                serializer = AcceptFavouriteRequestSerializer(requested_data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    UserFavouriteList.objects.create(userid=follow_acceptuser,favourite_userid=follow_requesteduser)
                    UserFavouriteList.objects.create(userid=follow_requesteduser,favourite_userid=follow_acceptuser)
                    
                    UserFavoutireRequestSend.objects.filter(Q(userid__exact=follow_acceptuser) & 
                                        Q(favourite_request_to__exact=follow_requesteduser)).update(is_favourite_accept=True)
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
        if request.data['is_favourite_reject'] == True:
            if UserFavoutireRequestSend.objects.filter(Q(favourite_request_to__exact=user.userid) & 
                                                    Q(id__exact=requestid)& Q(is_favourite_reject=False)).exists():    
                requested_data = self.get_object(requestid)
                serializer = RejectFavouriteRequestSerializer(requested_data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Bad Request",status=status.HTTP_400_BAD_REQUEST)




class FavouritesList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class= UserFavouriteListSerializer

    def get_queryset(self):
            user = self.request.user
            return UserFavouriteList.objects.filter(userid=user.userid)
    
    def list(self, request):

        queryset = self.get_queryset()
        serializer = UserFavouriteListSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)  
        # return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)






