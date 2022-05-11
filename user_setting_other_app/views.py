from multiprocessing import context
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import StaticSettingData, Notification, User_settings
from auth_user_app.models import User
from .serializers import (
    UserIndustryDataSerializer,
    UserAreaOfExperienceDataSerializer,
    UserInterestedAreaDataSerializer,
    UserGoalDataSerializer,
    ConsultancyServiceCategoryDataSerializer,
    CreateOtherRowsInStatictableSerializer,
    BlogTagDataSerializers,
    UserEducationDataSerializer,
    FacingtroubleSerializer,
    FaqSerializer,
    privacypolicySerializer,
    notificationSerializer,
    updateNotificationStatusSerializer,
    DeleteNotificationSerializer,
    UserSettingsOptionViewSerializer,
    EducationServiceDataSerializer,
    OverseasRecruitmentServiceDataSerializer,
    MedicalConsultancyServiceDataSerializer,
    LegalCivilServiceDataSerializer,
    PropertyManagementServiceDataSerializer,
    TourismServiceDataSerializer,
    TrainingServiceDataSerializer,
    DigitalServiceDataSerializer,
    TradeFacilitationServiceDataSerializer,
)
from auth_user_app.utils import Util
from django.db.models import Q
from django.db.models import F

from probashi_backend.renderers import UserRenderer


class CreateOtherRowsInStaticTableView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated,]

    # permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.all()
    serializer_class = CreateOtherRowsInStatictableSerializer
    renderer_classes = [UserRenderer]


class UserIndustryDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(user_industry_data__isnull=False)
    serializer_class = UserIndustryDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserIndustryDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {
            "user_industry_data": serializer.errors["user_industry_data"][0]
        }
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserIndustryDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class UserAreaOfExperienceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        user_areaof_experience_data__isnull=False
    )
    serializer_class = UserAreaOfExperienceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserAreaOfExperienceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {
            "user_areaof_experience_data": serializer.errors[
                "user_areaof_experience_data"
            ][0]
        }
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserAreaOfExperienceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class UserInterestedAreaDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(user_interested_area_data__isnull=False)
    serializer_class = UserInterestedAreaDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserInterestedAreaDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {
            "user_interested_area_data": serializer.errors["user_interested_area_data"][
                0
            ]
        }
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserInterestedAreaDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class UserGoalDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(user_goal_data__isnull=False)
    serializer_class = UserGoalDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserGoalDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserGoalDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class ConsultancyServiceCategoryDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        consultancyservice_category_data__isnull=False
    )
    serializer_class = ConsultancyServiceCategoryDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = ConsultancyServiceCategoryDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {
            "consultancyservice_category_data": serializer.errors[
                "consultancyservice_category_data"
            ][0]
        }
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConsultancyServiceCategoryDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class BlogTagDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(blog_tags_data__isnull=False)
    serializer_class = BlogTagDataSerializers
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = BlogTagDataSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"blog_tags_data": serializer.errors["blog_tags_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogTagDataSerializers(queryset, many=True)
        # context = {"data":serializer.data}
        tags = []
        for data in serializer.data:
            data["blog_tags_data"] = data["blog_tags_data"].split(",")
            # print(data['blog_tags_data'])
            tags += data["blog_tags_data"]
        # print(tags)
        context = {"data": tags}
        return Response(context, status=status.HTTP_200_OK)


class UserEducationDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(user_education_data__isnull=False)
    serializer_class = UserEducationDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = UserEducationDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {
            "user_education_data": serializer.errors["user_education_data"][0]
        }
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserEducationDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class FatchingTrubleView(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    # queryset = StaticSettingData.objects.filter(fatching_truble__isnull=False)
    serializer_class = FacingtroubleSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = FacingtroubleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # print(serializer.errors)
        # errorcontext = {'fatching_truble': serializer.errors['fatching_truble'][0]}
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     serializer = FacingtroubleSerializer(queryset, many=True)
    #     context = {"data":serializer.data}
    #     return Response(context, status=status.HTTP_200_OK)


class FaqView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(faq_title__isnull=False)
    serializer_class = FaqSerializer
    renderer_classes = [UserRenderer]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = FaqSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class privacypolicyView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(privacypolicy_title__isnull=False)
    serializer_class = privacypolicySerializer
    renderer_classes = [UserRenderer]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = privacypolicySerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class NotificationView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    # queryset = Notification.objects.filter(user_id=request.user)
    # serializer_class= notificationSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        user = request.user
        if request.data["userid"] == user.userid:
            serializer = notificationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                if User_settings.objects.filter(
                    Q(userid=user.userid) & Q(user_mail_notification_enable=True)
                ).exists():

                    email_body = f"""Hello,{user.user_fullname} \n You Have an notification about {serializer.data['notification_title']}"""

                    data = {
                        "email_body": email_body,
                        "to_email": user.user_email,
                        "email_subject": "Probashi Notification",
                    }

                    Util.send_email(data)

                return Response(serializer.data, status=status.HTTP_200_OK)
            errorcontext = {"notification": serializer.errors}
            return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        # print("::::::::",user.userid)
        return Notification.objects.filter(
            Q(userid=user.userid) & Q(is_notification_delete=False)
        )

    def list(self, request):
        user = request.user
        if request.data["userid"] == user.userid:
            queryset = self.get_queryset()
            serializer = notificationSerializer(queryset, many=True)
            context = {"data": serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)


# need to remove 30 days previous notification from table


class updateNotificationStatusView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_notification(self, notificationid):
        try:
            return Notification.objects.get(id__exact=notificationid)
        except Notification.DoesNotExist:
            raise Http404

    # def get(self,request,notificationid):
    #     notificationid = self.get_notification(notificationid)
    #     serializer = updateNotificationStatusSerializer(notificationid)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, notificationid):
        notificationid = self.get_notification(notificationid)
        serializer = updateNotificationStatusSerializer(
            notificationid, data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteNotificationView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_notification(self, notificationid):
        try:
            return Notification.objects.get(id__exact=notificationid)
        except Notification.DoesNotExist:
            raise Http404

    # def get(self,request,notificationid):
    #     notificationid = self.get_notification(notificationid)
    #     serializer = updateNotificationStatusSerializer(notificationid)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, notificationid):
        notificationid = self.get_notification(notificationid)
        serializer = DeleteNotificationSerializer(notificationid, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSettingsOptionView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_user(self, userid):
        try:
            return User_settings.objects.get(userid__exact=userid)
        except User_settings.DoesNotExist:
            raise Http404

    def get(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserSettingsOptionViewSerializer(userid)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, userid):
        userid = self.get_user(userid)
        serializer = UserSettingsOptionViewSerializer(userid, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------x----------------------------x-------------------------


class SpecificConsultancyData(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    renderer_classes = [UserRenderer]

    def get(self, request):
        param = request.query_params.get("service")
        # print( "request.data::::::::",param)
        if param == "Digital Service":
            print("Digital Service", param)
            data0 = StaticSettingData.objects.filter(
                Q(digitalservice_type__isnull=False)
            ).values_list("digitalservice_type")

            # print("data::::::::",data)
            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Education Service":
            data0 = StaticSettingData.objects.filter(
                Q(educationService_degree__isnull=False)
            ).values_list("educationService_degree")

            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Immigration Consultancy Service":
            data = {"subcategory1": [], "subcategory2": [], "subcategory3": []}
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Legal and Civil Service":
            data0 = StaticSettingData.objects.filter(
                Q(legalcivilservice_required__isnull=False)
            ).values_list("legalcivilservice_required")
            data1 = StaticSettingData.objects.filter(
                Q(legalcivilservice_issue__isnull=False)
            ).values_list("legalcivilservice_issue")
            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [item[0] for item in data1],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Medical Consultancy Service":
            data0 = StaticSettingData.objects.filter(
                medicalconsultancyservice_treatment_area__isnull=False
            ).values_list("medicalconsultancyservice_treatment_area")

            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Overseas Recruitment Service":
            data0 = StaticSettingData.objects.filter(
                overseasrecruitmentservice_job_type__isnull=False
            ).values_list("overseasrecruitmentservice_job_type")

            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Property Management Service":
            data0 = StaticSettingData.objects.filter(
                Q(propertymanagementservice_propertylocation__isnull=False)
            ).values_list("propertymanagementservice_propertylocation")
            data1 = StaticSettingData.objects.filter(
                Q(propertymanagementservice_type__isnull=False)
            ).values_list("propertymanagementservice_type")
            data2 = StaticSettingData.objects.filter(
                Q(propertymanagementservice_need__isnull=False)
            ).values_list("propertymanagementservice_need")

            # print('data=====', [item[0] for item in data0])
            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [item[0] for item in data1],
                "subcategory3": [item[0] for item in data2],
            }
            # print(data)
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Tourism Service":
            data0 = StaticSettingData.objects.filter(
                tourismservices__isnull=False
            ).values_list("tourismservices")

            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        elif param == "Trade Facilitation Service":
            data0 = StaticSettingData.objects.filter(
                Q(tradefacilitationservice_type__isnull=False)
            ).values_list("tradefacilitationservice_type")
            data1 = StaticSettingData.objects.filter(
                Q(tradefacilitationservice_Purpose__isnull=False)
            ).values_list("tradefacilitationservice_Purpose")

            # print('data::::::::::::',data)
            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [item[0] for item in data1],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        #
        elif param == "Training Service":
            data0 = StaticSettingData.objects.filter(
                Q(trainingservice_topic__isnull=False)
            ).values_list("trainingservice_topic")
            data1 = StaticSettingData.objects.filter(
                Q(trainingservice_duration__isnull=False)
            ).values_list("trainingservice_duration")

            data = {
                "subcategory1": [item[0] for item in data0],
                "subcategory2": [item[0] for item in data1],
                "subcategory3": [],
            }
            resp = {"data": data}
            return Response(resp, status=status.HTTP_200_OK)

        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class EducationServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(educationService_degree__isnull=False)
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = EducationServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # print( "request.data::::::::",request.query_params.get('service'))
        queryset = self.get_queryset()
        serializer = EducationServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class OverseasRecruitmentServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        overseasrecruitmentservice_job_type__isnull=False
    )
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = OverseasRecruitmentServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = OverseasRecruitmentServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class MedicalConsultancyServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        medicalconsultancyservice_treatment_area__isnull=False
    )
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = MedicalConsultancyServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = MedicalConsultancyServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class LegalCivilServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        Q(legalcivilservice_required__isnull=False)
        | Q(legalcivilservice_issue__isnull=False)
    )
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = LegalCivilServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = LegalCivilServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class PropertyManagementServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        Q(propertymanagementservice_propertylocation__isnull=False)
        | Q(propertymanagementservice_type__isnull=False)
        | Q(propertymanagementservice_need__isnull=False)
    )
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = PropertyManagementServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PropertyManagementServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class TourismServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(Q(tourismservices__isnull=False))
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = TourismServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TourismServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class TrainingServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        Q(trainingservice_topic__isnull=False)
        | Q(trainingservice_duration__isnull=False)
    )
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = TrainingServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TrainingServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class DigitalServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(Q(digitalservice_type__isnull=False))
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = DigitalServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DigitalServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


class TradeFacilitationServiceDataView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = StaticSettingData.objects.filter(
        Q(tradefacilitationservice_type__isnull=False)
        | Q(tradefacilitationservice_Purpose__isnull=False)
    )
    # serializer_class= EducationServiceDataSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        serializer = TradeFacilitationServiceDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        errorcontext = {"user_goal_data": serializer.errors["user_goal_data"][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TradeFacilitationServiceDataSerializer(queryset, many=True)
        context = {"data": serializer.data}
        return Response(context, status=status.HTTP_200_OK)


"""
'digitalservice_type', 'educationService_degree', 
'legalcivilservice_required', 'legalcivilservice_issue',
'medicalconsultancyservice_treatment_area', 'overseasrecruitmentservice_job_type',
'propertymanagementservice_propertylocation','propertymanagementservice_type','propertymanagementservice_need',
'tourismservices','tradefacilitationservice_type', 'tradefacilitationservice_Purpose',
'trainingservice_topic', 'trainingservice_duration'
"""
