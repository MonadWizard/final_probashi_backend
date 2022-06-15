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
    unmatch_useresSerializer
)
from .models import UserFavoutireRequestSend, UserFavouriteList, FriendsSuggation
from django.db.models import Q
from itertools import chain
from django.db.models import F
from probashi_backend.renderers import UserRenderer
from user_profile_app.models import User_education
from consultancy_app.models import ConsultancyCreate
from user_connection_app.utility import match_friends
from .helper_filter import *


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
            user_data = FriendsSuggation.objects.get(user=user)
        except:
            user_data = None

        if user_data is not None:
            match_all = []
            match_all = user_data.location if user_data.location else match_all
            match_all = (
                list(chain(match_all, user_data.goals))
                if user_data.goals
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.interest))
                if user_data.interest
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.durationyear_abroad))
                if user_data.durationyear_abroad
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.current_location_durationyear))
                if user_data.current_location_durationyear
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.industry))
                if user_data.industry
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.areaof_experience))
                if user_data.areaof_experience
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.industry_experienceyear))
                if user_data.industry_experienceyear
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.serviceholder))
                if user_data.serviceholder
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.selfemployed))
                if user_data.selfemployed
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.currentdesignation))
                if user_data.currentdesignation
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.company_name))
                if user_data.company_name
                else match_all
            )
            match_all = (
                list(chain(match_all, user_data.office_address))
                if user_data.office_address
                else match_all
            )

            # print(":::::::::::::::::", match_all)
            match_all = list(set(match_all))
            try:
                unmatch_all = list(set(User.objects.get(userid=user).user_unmatch))
            except Exception as e:
                unmatch_all = []
                
            for element in unmatch_all:
                if element in match_all:
                    match_all.remove(element)

            match_friend_data = [
                user := User.objects.filter(userid=x).values(
                    "userid",
                    "user_fullname",
                    "user_areaof_experience",
                    "user_photopath",
                    "is_consultant",
                )[0]
                for x in match_all
                if User.objects.filter(userid=x).exists()
            ]
            context = {"success": True, "data": match_friend_data}
            return Response(context, status=status.HTTP_200_OK)

        else:
            return Response(
                {"success": False, "message": "No match found!"},
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

    def delete_match_user(self, from_user, to_user):
        try:
            friends_suggation_obj = FriendsSuggation.objects.get(user__userid=from_user)
        except:
            friends_suggation_obj = None

        if friends_suggation_obj:
            if (
                friends_suggation_obj.location
                and to_user in friends_suggation_obj.location
            ):
                friends_suggation_obj.location.remove(to_user)
            if friends_suggation_obj.goals and to_user in friends_suggation_obj.goals:
                friends_suggation_obj.goals.remove(to_user)
            if (
                friends_suggation_obj.interest
                and to_user in friends_suggation_obj.interest
            ):
                friends_suggation_obj.interest.remove(to_user)
            if (
                friends_suggation_obj.durationyear_abroad
                and to_user in friends_suggation_obj.durationyear_abroad
            ):
                friends_suggation_obj.durationyear_abroad.remove(to_user)
            if (
                friends_suggation_obj.current_location_durationyear
                and to_user in friends_suggation_obj.current_location_durationyear
            ):
                friends_suggation_obj.current_location_durationyear.remove(to_user)
            if (
                friends_suggation_obj.industry
                and to_user in friends_suggation_obj.industry
            ):
                friends_suggation_obj.industry.remove(to_user)
            if (
                friends_suggation_obj.areaof_experience
                and to_user in friends_suggation_obj.areaof_experience
            ):
                friends_suggation_obj.areaof_experience.remove(to_user)
            if (
                friends_suggation_obj.industry_experienceyear
                and to_user in friends_suggation_obj.industry_experienceyear
            ):
                friends_suggation_obj.industry_experienceyear.remove(to_user)
            if (
                friends_suggation_obj.serviceholder
                and to_user in friends_suggation_obj.serviceholder
            ):
                friends_suggation_obj.serviceholder.remove(to_user)
            if (
                friends_suggation_obj.selfemployed
                and to_user in friends_suggation_obj.selfemployed
            ):
                friends_suggation_obj.selfemployed.remove(to_user)
            if (
                friends_suggation_obj.currentdesignation
                and to_user in friends_suggation_obj.currentdesignation
            ):
                friends_suggation_obj.currentdesignation.remove(to_user)
            if (
                friends_suggation_obj.company_name
                and to_user in friends_suggation_obj.company_name
            ):
                friends_suggation_obj.company_name.remove(to_user)
            if (
                friends_suggation_obj.office_address
                and to_user in friends_suggation_obj.office_address
            ):
                friends_suggation_obj.office_address.remove(to_user)
            friends_suggation_obj.save()

    def create(self, request):
        user = self.request.user
        if request.data["userid"] == user.userid:
            if UserFavoutireRequestSend.objects.filter(
                Q(userid__exact=user.userid)
                & Q(favourite_request_to__exact=request.data["favourite_request_to"])
            ).exists():
                return Response(
                    "You already send request to this user",
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
                    self.delete_match_user(
                        user.userid, request.data["favourite_request_to"]
                    )
                    self.delete_match_user(
                        request.data["favourite_request_to"], user.userid
                    )
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
            print("residential location:::::::::", residential_location)
            residential_location_data = [
                "Bangladesh," + x for x in residential_location if x != ""
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

    def get_user(self, data, user):
        education_data = data["education_data"]
        industry_data = data["industry_data"]
        service_type = data["service_type"]
        location_data = data["location_data"]
        location_city_r = []
        location_city_nr = []

        all_user = User.objects.filter(
            ~Q(userid=user.userid) & ~Q(is_staff=True) & Q(is_active=True)
        ).values("userid")

        for location in location_data:
            if location.split(",")[0] == "Bangladesh":
                location_city_r.append(location.split(",")[1])
            else:
                location_city_nr.append(location.split(",")[1])

        if data["education_data"] != []:
            education_queryset = User_education.objects.all().values("userid")
            education_queryset = filterby_userEduDegree(
                education_queryset, education_data
            ).values("userid")
        else:
            education_queryset = None

        user_queryset = User.objects.all().values("userid")
        user_queryset = filterby_userIndustry(user_queryset, industry_data).values(
            "userid"
        )
        user_queryset = filterby_residentialDistrict(
            user_queryset, location_city_r
        ).values("userid")

        user_queryset = filterby_nonresidentialCity(
            user_queryset, location_city_nr
        ).values("userid")

        if data["service_type"] != []:
            service_queryset = ConsultancyCreate.objects.all().values("userid")
            service_queryset = filterby_consultantServiceCategory(
                service_queryset, service_type
            ).values("userid")
        else:
            service_queryset = None

        try:
            if service_queryset and education_queryset:
                # print(" service and edu exist")
                search_data = all_user.intersection(
                    user_queryset, education_queryset, service_queryset
                )
                return search_data
            if education_queryset and not service_queryset:
                # print(" edu exist")
                search_data = all_user.intersection(user_queryset, education_queryset)
                return search_data
            if service_queryset and not education_queryset:
                # print(" service exist")
                search_data = all_user.intersection(user_queryset, service_queryset)
                return search_data
            else:
                # print("all user data")
                return all_user.intersection(user_queryset)

        except:
            return []

    def post(self, request):
        user = self.request.user
        data = request.data
        search_user = self.get_user(data, user)

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

    def get_user(self, data, user):
        user_name = data["user_fullname"]
        search_data = User.objects.filter(
            ~Q(userid=user.userid)
            & ~Q(is_staff=True)
            & (
                Q(user_fullname__icontains=user_name)
                | Q(user_username__icontains=user_name)
            )
        )
        return search_data

    def post(self, request):
        user = self.request.user
        data = request.data
        search_user = self.get_user(data, user)
        serializer = UserSearchFieldSerializer(search_user, many=True)
        paginator = UserSearchFilterPagination()
        page = paginator.paginate_queryset(serializer.data, request)
        if page is not None:
            return paginator.get_paginated_response(page)
        return Response(page, status=status.HTTP_200_OK)



class unmatch_useres(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, userid):
        userid = self.get_user(userid)
        serializer = unmatch_useresSerializer(userid)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, userid):
        userid = self.get_user(userid)
        user = request.user
        if request.data != {}:
            try:
                unmatch_exist = User.objects.get(userid=user.userid).user_unmatch
                new_match = unmatch_exist + [request.data["user_unmatch"]]
                update_unmatch = {"user_unmatch": new_match}
                # print("new_match", new_match)
            except Exception as e:
                update_unmatch = {"user_unmatch": [request.data["user_unmatch"]]}

            serializer = unmatch_useresSerializer(userid, data=update_unmatch)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        errorContext = {"error": "No data found"}
        return Response(errorContext, status=status.HTTP_400_BAD_REQUEST)





