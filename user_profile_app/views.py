from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework import permissions
from django.http import Http404
from django.db.models import Q
from probashi_backend.renderers import UserRenderer
from auth_user_app.models import User
from .models import (
    User_socialaccount_and_about,
    User_experience,
    User_education,
    User_idverification,
)
from .serializers import (
    UserProfileSkipPart0Serializer,
    UserProfileSkipPart1Serializer,
    UserProfileSkipPart2Serializer,
    UserEditPrifileSerializer,
    UserSocialaccountAboutSerializer,
    UserSocialaccountAboutUpdatSerializer,
    UserExperienceCreateSerializer,
    UserEducationCreateSerializer,
    UserIdVerificationCreateSerializer,
    UserProfileViewSerializer,
    UserEditPrifileWithoutImageSerializer,
    UserInterestedAreaSerializer,
    UserGoalSerializer,
    UserProfileWithConsultancyViewSerializer,
)

from probashi_backend.renderers import UserRenderer


class UserProfileSkipPart0(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User.objects.get(userid=userid)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserProfileSkipPart0Serializer(userid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileSkipPart1(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User.objects.get(userid=userid)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserProfileSkipPart1Serializer(userid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileSkipPart2(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserProfileSkipPart2Serializer(userid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEditProfile(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User.objects.get(userid__exact=userid)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserEditPrifileSerializer(userid)
        return Response(serializer.data)

    def put(self, request, userid):
        userid = self.get_user(userid)

        if request.data["user_photopath"] == "":
            serializer = UserEditPrifileWithoutImageSerializer(
                userid, data=request.data
            )
        else:
            serializer = UserEditPrifileSerializer(userid, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInterestedAreaView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserInterestedAreaSerializer(userid)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, userid):
        userid = self.get_user(userid)
        if request.data != {}:
            serializer = UserInterestedAreaSerializer(userid, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        errorContext = {"error": "No data found"}
        return Response(errorContext, status=status.HTTP_400_BAD_REQUEST)


class UserGoalView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User.objects.get(pk=userid)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserGoalSerializer(userid)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, userid):
        userid = self.get_user(userid)
        if request.data != {}:
            serializer = UserGoalSerializer(userid, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        errorContext = {"error": "No data found"}
        return Response(errorContext, status=status.HTTP_400_BAD_REQUEST)


class UserAboutSocialLinkUpdate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User_socialaccount_and_about.objects.get(userid__exact=userid)
        except User_socialaccount_and_about.DoesNotExist:
            raise Http404

    def get(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserSocialaccountAboutSerializer(userid)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserSocialaccountAboutUpdatSerializer(userid, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserExperienceCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserExperienceCreateSerializer(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()
            context = {"data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEducationCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserEducationCreateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            context = {"data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserIdVerificationCreate(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserIdVerificationCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserProfileViewSerializer
    renderer_classes = [UserRenderer]

    def get_user(self):
        user = self.request.user
        try:
            return User.objects.get(userid=user.userid)

        except:
            return None

    def get_profile_persentage(self, data, user):
        complete_profile_persentage = 5
        if data["user_username"]:
            complete_profile_persentage += 5
        # skip 0
        if data["user_currentdesignation"]:
            complete_profile_persentage += 5
        #  skip 1
        if data["user_industry"]:
            complete_profile_persentage += 5
        #  skip 2
        if data["user_interested_area"]:
            complete_profile_persentage += 5
        #  about
        if data["user_socialaboutdata"].get("user_about"):
            if len(data["user_socialaboutdata"].get("user_about")) > 2:
                complete_profile_persentage += 5
        #  social links
        if (
            data["user_socialaboutdata"].get("user_fbaccount")
            or data["user_socialaboutdata"].get("user_twitteraccount")
            or data["user_socialaboutdata"].get("user_instagramaccount")
            or data["user_socialaboutdata"].get("user_linkedinaccount")
            or data["user_socialaboutdata"].get("user_website")
        ) and (
            int(len(data["user_socialaboutdata"].get("user_fbaccount")))
            > 2
            or int(
                len(
                    data["user_socialaboutdata"].get(
                        "user_twitteraccount"
                    )
                )
            )
            > 2
            or int(
                len(
                    data["user_socialaboutdata"].get(
                        "user_instagramaccount"
                    )
                )
            )
            > 2
            or int(
                len(
                    data["user_socialaboutdata"].get(
                        "user_linkedinaccount"
                    )
                )
            )
            > 2
            or int(len(data["user_socialaboutdata"].get("user_website")))
            > 2
        ):
            complete_profile_persentage += 5
        #  contact link
        if (
            data["user_socialaboutdata"].get("user_whatsapp_account")
            or data["user_socialaboutdata"].get("user_viber_account")
            or data["user_socialaboutdata"].get("user_immo_account")
        ) and (
            int(
                len(
                    data["user_socialaboutdata"].get(
                        "user_whatsapp_account"
                    )
                )
            )
            > 2
            or int(
                len(
                    data["user_socialaboutdata"].get(
                        "user_viber_account"
                    )
                )
            )
            > 2
            or int(
                len(
                    data["user_socialaboutdata"].get("user_immo_account")
                )
            )
            > 2
        ):

            complete_profile_persentage += 5
        #  experience
        if data["user_experiencedata"] != []:
            complete_profile_persentage += 15
        #  education
        if data["user_educationdata"] != []:
            complete_profile_persentage += 20
        #  id verification
        if data["user_idverificationdata"] != []:
            complete_profile_persentage += 25

        if complete_profile_persentage == 100:
            user.user_profile_status = True
            user.save()

        dic_serializer = dict(data)
        dic_serializer["profile_complete_percentage"] = complete_profile_persentage
        context = {"data": dic_serializer}
        return context

    

    def list(self, request):

        user = self.get_user()
        if user.is_consultant:
            serializer = UserProfileWithConsultancyViewSerializer(user)
            return Response( self.get_profile_persentage(serializer.data, user), status=status.HTTP_200_OK)

        else:
            serializer = UserProfileViewSerializer(user)
            return Response(self.get_profile_persentage(serializer.data, user)
                , status=status.HTTP_200_OK)

