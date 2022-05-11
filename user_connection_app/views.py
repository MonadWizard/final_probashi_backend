from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from django.http import Http404
from auth_user_app.models import User
from .serializers import SerachUserSerializer
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from user_profile_app.serializers import (
    UserProfileViewSerializer,
    UserProfileWithConsultancyViewSerializer,
)
from .serializers import (
    UserFavouriteRequestSendSerializer,
    UserFavouriteRequestsSerializer,
    AcceptFavouriteRequestSerializer,
    RejectFavouriteRequestSerializer,
    UserFavouriteListSerializer,
    UserSearchFieldSerializer,
)
from .models import UserFavoutireRequestSend, UserFavouriteList, FriendsSuggation
from django.db.models import Q
from itertools import chain
from django.db.models import F
from probashi_backend.renderers import UserRenderer
from user_profile_app.models import User_education
from consultancy_app.models import ConsultancyCreate
from user_connection_app.utility import match_friends
import itertools


class TakeMatchFriend(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        match_friends(user_id=user.userid)
        return Response("matching prepaired", status=status.HTTP_200_OK)


class GetMatchFriendSetPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"


class Friends_suggation(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserFavouriteRequestsSerializer

    def get(self, request):
        user = request.user.userid

        try:
            user_data = FriendsSuggation.objects.filter(user=user)
        except:
            user_data = None
        match_all = user_data.values("location", "goals", "interest")[0]
        match_12 = user_data.values("location", "goals")[0]
        match_13 = user_data.values("location", "interest")[0]
        match_23 = user_data.values("goals", "interest")[0]
        match_1 = user_data.values("location")[0]
        match_2 = user_data.values("goals")[0]
        match_3 = user_data.values("interest")[0]

        try:
            match_marge = {
                **match_all,
                **match_12,
                **match_13,
                **match_23,
                **match_1,
                **match_2,
                **match_3,
            }
            match_friend_all = [list(set(x)) for x in match_marge.values() if x != []]
            match_friend_all = list(itertools.chain.from_iterable(match_friend_all))
            match_friend_data = [
                User.objects.filter(userid=x).values(
                    "userid",
                    "user_fullname",
                    "user_areaof_experience",
                    "user_photopath",
                    "is_consultant",
                )[0]
                for x in match_friend_all
            ]
            context = {"success": True, "data": match_friend_data}
            return Response(context, status=status.HTTP_200_OK)

        except Exception as e:
            # print("error:::::", e)
            return Response(
                {"success": False, "message": "No match found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class GetAllusersSetPagination(PageNumberPagination):
    page_size = 15
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
    serializer_class = UserProfileViewSerializer

    def get_object(self, user_id):
        try:
            return User.objects.get(userid=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        user_id = user_id
        data = self.get_object(user_id)

        if User.objects.filter(Q(is_consultant=False) & Q(userid=data.userid)).exists():
            serializer = self.serializer_class(data)
            context = {"data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        elif User.objects.filter(
            Q(is_consultant=True) & Q(userid=data.userid)
        ).exists():
            serializer = UserProfileWithConsultancyViewSerializer(data)
            context = {"data": serializer.data}
            # print(context)
            return Response(context, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class FavouriteRequestSendView(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = UserFavoutireRequestSend.objects.all()
    serializer_class = UserFavouriteRequestSendSerializer
    renderer_classes = [UserRenderer]

    def create(self, request):
        user = self.request.user
        if request.data["userid"] == user.userid:
            if UserFavoutireRequestSend.objects.filter(
                Q(userid__exact=user.userid)
                & Q(favourite_request_to__exact=request.data["favourite_request_to"])
            ).exists():
                return Response(
                    "You can not send request to same user",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if UserFavouriteList.objects.filter(
                Q(userid__exact=user.userid)
                & Q(favourite_userid__exact=request.data["favourite_request_to"])
            ).exists():
                return Response(
                    "You are Already Friend", status=status.HTTP_400_BAD_REQUEST
                )
            else:
                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class FavouriteRequestsView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserFavouriteRequestsSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        user = self.request.user
        return UserFavoutireRequestSend.objects.filter(
            Q(favourite_request_to=user.userid)
            & Q(is_favourite_accept=False)
            & Q(is_favourite_reject=False)
        )

    def list(self, request, format=None):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class AcceptFavouriteRequest(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]
    serializer_class = AcceptFavouriteRequestSerializer

    def get_object(self, requestid):
        try:
            return UserFavoutireRequestSend.objects.get(id=requestid)
        except UserFavoutireRequestSend.DoesNotExist:
            raise Http404

    def put(self, request, requestid):
        user = self.request.user

        if request.data["is_favourite_accept"] == True:
            if UserFavoutireRequestSend.objects.filter(
                Q(favourite_request_to__exact=user.userid)
                & Q(id__exact=requestid)
                & Q(is_favourite_accept=False)
            ).exists():
                requested_data = self.get_object(requestid)
                follow_acceptuser = requested_data.favourite_request_to
                follow_requesteduser = requested_data.userid
                serializer = self.serializer_class(requested_data, data=request.data)
                
                if serializer.is_valid():
                    serializer.save()
                    UserFavouriteList.objects.create(
                        userid=follow_acceptuser, favourite_userid=follow_requesteduser
                    )
                    UserFavouriteList.objects.create(
                        userid=follow_requesteduser, favourite_userid=follow_acceptuser
                    )
                    UserFavoutireRequestSend.objects.filter(
                        Q(userid__exact=follow_acceptuser)
                        & Q(favourite_request_to__exact=follow_requesteduser)
                    ).update(is_favourite_accept=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class RejectFavouriteRequest(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]
    serializer_class = RejectFavouriteRequestSerializer

    def get_object(self, requestid):
        try:
            return UserFavoutireRequestSend.objects.get(id=requestid)
        except UserFavoutireRequestSend.DoesNotExist:
            raise Http404

    def put(self, request, requestid):
        user = self.request.user
        if request.data["is_favourite_reject"] == True:
            if UserFavoutireRequestSend.objects.filter(
                Q(favourite_request_to__exact=user.userid)
                & Q(id__exact=requestid)
                & Q(is_favourite_reject=False)
            ).exists():
                requested_data = self.get_object(requestid)
                serializer = self.serializer_class(requested_data, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class FavouritesList(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserFavouriteListSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        user = self.request.user
        return UserFavouriteList.objects.filter(userid=user.userid)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class UserSearchGetData(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        user = self.request.user
        if User.objects.filter(userid=user.userid).exists():
            education_data = set(
                User_education.objects.exclude(
                    user_edu_degree__isnull=True
                ).values_list("user_edu_degree", flat=True)
            )
            industry_data = set(
                User.objects.exclude(user_industry__isnull=True).values_list(
                    "user_industry", flat=True
                )
            )
            residential_location = list(
                set(
                    User.objects.exclude(
                        user_residential_district__isnull=True
                    ).values_list("user_residential_district", flat=True)
                )
            )
            residential_location_data = [
                "Bangladesh," + x for x in residential_location
            ]
            nonresidential_location = list(
                set(
                    User.objects.exclude(
                        user_nonresidential_city__isnull=True
                    ).values_list(
                        "user_nonresidential_country", "user_nonresidential_city"
                    )
                )
            )
            for i in range(len(nonresidential_location)):
                nonresidential_location[i] = (
                    nonresidential_location[i][0] + "," + nonresidential_location[i][1]
                )
            location_data = residential_location_data + nonresidential_location
            service_type = set(
                ConsultancyCreate.objects.exclude(
                    consultant_service_category__isnull=True
                ).values_list("consultant_service_category", flat=True)
            )
            context = {
                "success": True,
                "education_data": education_data,
                "industry_data": industry_data,
                "location_data": location_data,
                "service_type": service_type,
            }
            return Response(context, status=status.HTTP_200_OK)
        err_context = {"success": False, "message": "User not found"}
        return Response(err_context, status=status.HTTP_400_BAD_REQUEST)


class UserSearchFilterPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"


class UserSearchFilter(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    renderer_classes = [UserRenderer]

    def get_user(self, data):
        education_data = data["education_data"]
        industry_data = data["industry_data"]
        service_type = data["service_type"]
        location_data = data["location_data"]
        location_city = []

        for location in location_data:
            city = location.split(",")[1]
            location_city.append(city)
        
        education_search_data = (
            User_education.objects.filter(user_edu_degree__in=education_data)
            .values("userid")
            .distinct()
        )
        user_filter_data = (
            User.objects.filter(
                Q(user_industry__in=industry_data)
                | Q(user_residential_district__in=location_city)
                | Q(user_nonresidential_city__in=location_city)
                | Q(is_active=True)
            )
            .values("userid")
            .distinct()
        )
        service_type_search_data = (
            ConsultancyCreate.objects.filter(
                consultant_service_category__in=service_type
            )
            .values("userid")
            .distinct()
        )
        search = list(
            chain(
                education_search_data,
                user_filter_data,
                service_type_search_data,
            )
        )
        search_data = [
            value for item in search for key, value in item.items() if key == "userid"
        ]
        return search_data

    def post(self, request):
        data = request.data
        # print(request.data)
        search_user = self.get_user(data)

        details = User.objects.filter(userid__in=search_user).values(
            "userid",
            "user_fullname",
            "user_areaof_experience",
            "user_geolocation",
            "user_photopath",
            "is_consultant",
        )
        paginator = UserSearchFilterPagination()
        page = paginator.paginate_queryset(details, request)
        if page is not None:
            return paginator.get_paginated_response(page)

        return Response(page, status=status.HTTP_200_OK)


class UserSearchField(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    renderer_classes = [UserRenderer]

    def get_user(self, data):
        user_name = data["user_fullname"]
        search_data = User.objects.filter(
            Q(user_fullname__contains=user_name) | Q(user_username__contains=user_name)
        )
        return search_data

    def post(self, request):
        user = self.request.user
        data = request.data
        search_user = self.get_user(data)
        serializer = UserSearchFieldSerializer(search_user, many=True)
        paginator = UserSearchFilterPagination()
        page = paginator.paginate_queryset(serializer.data, request)
        if page is not None:
            return paginator.get_paginated_response(page)
        return Response(page, status=status.HTTP_200_OK)
