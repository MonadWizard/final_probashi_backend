from multiprocessing import context
from unittest import result
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from yaml import serialize
from auth_user_app.models import User
from .serializers import SerachUserSerializer
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from user_profile_app.serializers import UserProfileViewSerializer, UserProfileWithConsultancyViewSerializer
from .serializers import (UserFavouriteRequestSendSerializer, UserFavouriteRequestsSerializer,
                        AcceptFavouriteRequestSerializer,RejectFavouriteRequestSerializer,
                        UserFavouriteListSerializer,UserSearchFieldSerializer)
from .models import UserFavoutireRequestSend, UserFavouriteList, FriendsSuggation
from django.db.models import Q
from itertools import chain
from django.db.models import F
import datetime
import json 
from probashi_backend.renderers import UserRenderer
from user_profile_app.models import User_education
from consultancy_app.models import ConsultancyCreate
from user_connection_app.utility import match_friends
from itertools import chain

class TakeMatchFriend(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # renderer_classes = [UserRenderer]

    def get(self, request):
        user = request.user
        # print('user:::::',user.userid)
        match_friends(user_id=user.userid)
        return Response('matching prepaired',status=status.HTTP_200_OK)


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





class GetMatchFriendSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    # max_page_size = 10000

    # page_size_query_param = 'page_size'

    # def get_paginated_response(self, data):
    #     next_url = self.get_next_link()
    #     previous_url = self.get_previous_link()

    #     if next_url is not None and previous_url is not None:
    #         link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev"'
    #     elif next_url is not None:
    #         link = '<{next_url}>; rel="next"'
    #     elif previous_url is not None:
    #         link = '<{previous_url}>; rel="prev"'
    #     else:
    #         link = ''

    #     link = link.format(next_url=next_url, previous_url=previous_url)
    #     # print('link:::',{'Link': link, 'Count': self.page.paginator.count}) if link else {}
    #     headers = {'Link': link, 'Count': self.page.paginator.count} if link else {}
    #     data = {'Link': link, 'Count': self.page.paginator.count, 'data': data}
    #     return Response(data, headers=headers)

class Friends_suggation(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class= UserFavouriteRequestsSerializer
    pagination_class = GetMatchFriendSetPagination
    # renderer_classes = [UserRenderer]

    def get(self,request):
        user = request.user.userid
        # print('user:::::',user)
        match_all = FriendsSuggation.objects.filter(user=user).values('location', 'goals', 'interest')[0]
        match_12 = FriendsSuggation.objects.filter(user=user).values('location', 'goals')[0]
        match_13 = FriendsSuggation.objects.filter(user=user).values('location', 'interest')[0]
        match_23 = FriendsSuggation.objects.filter(user=user).values('goals', 'interest')[0]
        match_1 = FriendsSuggation.objects.filter(user=user).values('location')[0]
        match_2 = FriendsSuggation.objects.filter(user=user).values('goals')[0]
        match_3 = FriendsSuggation.objects.filter(user=user).values('interest')[0]

        try:
            match_friend_all = set.intersection(*[set(x) for x in match_all.values()])
            match_friend_12 = set.intersection(*[set(x) for x in match_12.values()])
            match_friend_13 = set.intersection(*[set(x) for x in match_13.values()])
            match_friend_23 = set.intersection(*[set(x) for x in match_23.values()])
            match_friend_1 = set.intersection(*[set(x) for x in match_1.values()])
            match_friend_2 = set.intersection(*[set(x) for x in match_2.values()])
            match_friend_3 = set.intersection(*[set(x) for x in match_3.values()])

            # print("match friend all:::::::",match_friend_all)

            match_friend_id = set(chain(match_friend_all, match_friend_12, match_friend_13, match_friend_23,match_friend_1, match_friend_2, match_friend_3))
            match_friend_data = []
            for mf in match_friend_id:
                match_friend = User.objects.filter(userid=mf).values('userid', 'user_fullname', 'user_areaof_experience', 'user_photopath', 'is_consultant')[0]
                match_friend_data.append(match_friend)
            
# -------------------------paginator

            # print(type(match_friend_data),"::::::::::::::::::::::", match_friend_data)

            paginator = GetMatchFriendSetPagination()
            page = paginator.paginate_queryset(match_friend_data, request)
            if page is not None:
                # print("is not none::::::::::::::::::::::", page)
                return paginator.get_paginated_response(page)
            
            # print("::::::::::::::::::::::", page)

            return Response(page)


# ------------------------------------------------paginator
            context = {'success': True, 'data': match_friend_data}
            return Response(context)

        except Exception as e:
            # print("error:::::",e)
            return Response({
                'success': False,
                'message': 'No match found'
            }, status=status.HTTP_400_BAD_REQUEST)


        







class GetAllusersSetPagination(PageNumberPagination):
    page_size = 20
    # page_size_query_param = 'users'
    max_page_size = 10000

class GetAllUserPaginationView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SerachUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = GetAllusersSetPagination
    renderer_classes = [UserRenderer]


class GetSpecificUserView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

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
    renderer_classes = [UserRenderer]

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
    renderer_classes = [UserRenderer]

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
    renderer_classes = [UserRenderer]


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
    renderer_classes = [UserRenderer]

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
    renderer_classes = [UserRenderer]

    def get_queryset(self):
            user = self.request.user
            return UserFavouriteList.objects.filter(userid=user.userid)
    
    def list(self, request):

        queryset = self.get_queryset()
        serializer = UserFavouriteListSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)  
        # return Response('Bad Request', status=status.HTTP_400_BAD_REQUEST)



class UserSearchGetData(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    # renderer_classes = [UserRenderer]

    def get(self,request):
        user = self.request.user
        if User.objects.filter(userid=user.userid).exists():
            education_data = set(User_education.objects.exclude(user_edu_degree__isnull=True).values_list('user_edu_degree', flat=True))
            industry_data = set(User.objects.exclude(user_industry__isnull=True).values_list('user_industry', flat=True))
            
            residential_location = list(set(User.objects.exclude(user_residential_district__isnull=True).values_list('user_residential_district', flat=True)))
            residential_location_data = ['Bangladesh,'+x for x in residential_location]
            nonresidential_location = list(set(User.objects.exclude(user_nonresidential_city__isnull=True).values_list('user_nonresidential_country','user_nonresidential_city')))
            for i in range(len(nonresidential_location)):
                nonresidential_location[i] = nonresidential_location[i][0]+','+nonresidential_location[i][1]
            location_data = residential_location_data + nonresidential_location
            
            service_type = set(ConsultancyCreate.objects.exclude(consultant_service_category__isnull=True).values_list('consultant_service_category', flat=True))
            # print("location data:::::::::::::::::::",service_type)
            
            context = {"success": True, 
                        "education_data":education_data,
                        "industry_data":industry_data,
                        "location_data":location_data,
                        "service_type":service_type
                        }
            return Response(context, status=status.HTTP_200_OK)
        err_context = {"success": False, "message": "User not found"}
        return Response(err_context, status=status.HTTP_400_BAD_REQUEST)





class UserSearchFilterPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class UserSearchFilter(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    renderer_classes = [UserRenderer]

    def get_user(self,data):

        education_data = data['education_data']
        industry_data = data['industry_data']
        service_type = data['service_type']
        location_data = data['location_data']

        location_city = []
        for location in location_data:
            city = location.split(",")[1]
            location_city.append(city)

        education_search_data = User_education.objects.filter(user_edu_degree__in=education_data).values('userid')
        
        industry_search_data = User.objects.filter(user_industry__in=industry_data).values('userid')

        location_search_data_r = User.objects.filter(user_residential_district__in=location_city).values('userid')
        
        
        location_search_data_nr = User.objects.filter(user_nonresidential_city__in=location_city).values('userid')
        
        location_search_data = list(chain(location_search_data_r, location_search_data_nr))


        service_type_search_data = ConsultancyCreate.objects.filter(consultant_service_category__in=service_type).values('userid')


        search = list(chain(education_search_data,industry_search_data,location_search_data,service_type_search_data))

        search_data = set(val for dic in search for val in dic.values())

        # print("search data:::::::::::::::",search_data)

        return search_data

    def post(self,request):
        user = self.request.user
        data = request.data
        # print(request.data)
        search_user = self.get_user(data)

        details = User.objects.filter(userid__in=search_user).values(
                            'userid', 'user_fullname','user_areaof_experience','user_geolocation',
                            'user_photopath','is_consultant')
        
            
        # context = {"success":True,"data":details}
        paginator = UserSearchFilterPagination()
        page = paginator.paginate_queryset(details, request)
        if page is not None:
            return paginator.get_paginated_response(page)
        
        

        return Response(page, status=status.HTTP_200_OK)




class UserSearchField(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    renderer_classes = [UserRenderer]

    def get_user(self,data):

        user_name = data['user_fullname']
        
        search_data = User.objects.filter(user_fullname__contains=user_name)

        # print("search data:::::::::::::::",search_data)

        return search_data

    def post(self,request):
        user = self.request.user
        data = request.data

        # print(":::::::::::::::::::::",request.data)
        search_user = self.get_user(data)

        serializer = UserSearchFieldSerializer(search_user, many=True)
        # if serializer.is_valid():
            # context = {"success":True,"data":serializer.data}
            
        paginator = UserSearchFilterPagination()
        page = paginator.paginate_queryset(serializer.data, request)
        if page is not None:
            return paginator.get_paginated_response(page)
        

        return Response(page, status=status.HTTP_200_OK)
            
        # else:
        #     context = {"message":"User not found"}
        #     return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    


