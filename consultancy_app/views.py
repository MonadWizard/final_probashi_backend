import json
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework import permissions
from django.http import Http404
from .models import (
    ConsultancyCreate,
    UserConsultAppointmentRequest,
    ConsultancyTimeSchudile,
    ProUserPayment,
    ConsultancyPayment,
)

from .serializers import (
    ConsultancyCreateSerializer,
    ServiceCategorySerializer,
    ConsultancyTimeSchudileSerializer,
    GetAllServicesCategoryScheduleSerializer,
    GetAllCategoryNotTakingScheduleSerializer,
    GetAllCategoryScheduleSerializer,
    ConsultantAppointmentRequestSerializer,
    AppointmentSeeker_StarRatingSerializer,
    ConsultantProvider_StarRatingSerializer,
    AppointmentSeeker_MissingAppointmentReasonSerializer,
    GetSpecificCategoryServiceSearchDataSerializer,
    ConsultancyPaymentSerializer,
    ServiceSearchFilterSerializer,
)
from .sslcommerz_helper import (
    Pro_user_CREATE_and_GET_session,
    Consultancy_CREATE_and_GET_session,
    orderVerify,
)
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.db.models import Q
from auth_user_app.models import User
from itertools import chain

from .helper_filter import *

from probashi_backend.renderers import UserRenderer

from auth_user_app.utils import Util



class GetAllServicesCategoryView(generics.ListAPIView):
    serializer_class = ServiceCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        queryset = (
            ConsultancyCreate.objects.annotate()
            .values("consultant_service_category")
            .distinct()
        )
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class ConsultancyCreateView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = ConsultancyCreate.objects.all()
    serializer_class = ConsultancyCreateSerializer
    renderer_classes = [UserRenderer]

    def create(self, request):
        user = request.user
        if request.data["userid"] == user.userid:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()

                user.is_consultant = True
                user.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "You are not authorized to perform this action"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ConsultancyTimeSchudileView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultancyTimeSchudileSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        user = self.request.user
        try:
            queryset = ConsultancyTimeSchudile.objects.get(
                consultancyid__userid=user.userid
            )
            return queryset
        except:
            raise Http404

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConsultancyTimeSchudileSerializer(queryset, many=True)
        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        con_user = ConsultancyCreate.objects.filter(
            Q(userid=user.userid) & Q(id=request.data["consultancyid"])
        ).exists()
        if con_user == True:
            serializer = ConsultancyTimeSchudileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "incorrect consultancyid"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetAllServicesCategorySchedule(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetAllServicesCategoryScheduleSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        user = self.request.user

        queryset = ConsultancyCreate.objects.filter(userid=user.userid)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class SpecificServicesSchedules(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetAllServicesCategoryScheduleSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self, id):
        id = id
        queryset = ConsultancyCreate.objects.filter(Q(id=id))
        return queryset

    def list(self, request):
        id = request.query_params.get("id")
        queryset = self.get_queryset(id)
        serializer = self.serializer_class(queryset, many=True)
        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class ALLScheduils_forConsultancyProvider(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_object(self, user_id):
        try:
            return ConsultancyCreate.objects.filter(userid=user_id)
        except ConsultancyCreate.DoesNotExist:
            raise Http404

    def get(self, request):
        user_id = request.user.userid

        consultancy = self.get_object(user_id)

        serializer = GetAllCategoryScheduleSerializer(consultancy, many=True)
        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class NotTakingScheduil_forSpecificUser(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetAllCategoryNotTakingScheduleSerializer
    renderer_classes = [UserRenderer]

    def get_object(self, user_id):
        try:
            return ConsultancyCreate.objects.filter(Q(userid=user_id))
        except ConsultancyCreate.DoesNotExist:
            raise Http404

    def get(self, request):
        user_id = request.query_params.get("user_id")
        consultancy = self.get_object(user_id)

        serializer = self.serializer_class(consultancy, many=True)

        for i in serializer.data:
            if i["consultancy_timeschudiles"] == []:
                i["consultancy_timeschudiles"] = None

        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


class AppointmentSeeker_ConsultantRequest(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultancyPaymentSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):

        user = request.user

        try:
            consultancyTimeSchudile = ConsultancyTimeSchudile.objects.get(
                id=request.data["ConsultancyTimeSchudile"]
            )
        except Exception as e:
            return Response(
                "incorrect time schedule id", status=status.HTTP_400_BAD_REQUEST
            )
        if request.data["seekerid"] == user.userid and consultancyTimeSchudile != None:
            data = Consultancy_CREATE_and_GET_session(request, user)
            tran_id = data["post_body"]["tran_id"]

            if data["res"]["status"].lower() == "success":
                result = {}
                result["status"] = data["res"]["status"].lower()
                result["data"] = data["res"]["GatewayPageURL"]
                result["logo"] = data["res"]["storeLogo"]

                consultancy_paydata = {
                    "userid": user.userid,
                    "consultancy_sheduleid": request.data["ConsultancyTimeSchudile"],
                    "tran_id": tran_id,
                }
                serializer = self.serializer_class(data=consultancy_paydata)
                if serializer.is_valid():
                    serializer.save()

                    serializer = ConsultantAppointmentRequestSerializer(
                        data=request.data
                    )
                    if serializer.is_valid():
                        serializer.save()
                        return Response(result, status=status.HTTP_200_OK)
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {"message": "You are not authorized to make this request"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            else:
                return Response(
                    data["res"]["status"].lower(), status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            "seekerid or ConsultancyTimeSchudile invalid",
            status=status.HTTP_400_BAD_REQUEST,
        )


class IpnSslcommerze_pro(views.APIView):
    
    def post(self, request):


        if request.data:
            data = orderVerify(request)
            if data["status"] == "VALID":
                tran_id = data["tran_id"]

                if ProUserPayment.objects.filter(tran_id=tran_id).exists():
                    pro_user = ProUserPayment.objects.filter(tran_id=tran_id).values(
                        "userid"
                    )[0]["userid"]
                    User.objects.filter(userid=pro_user).update(is_pro_user=True)

                    ProUserPayment.objects.filter(tran_id=tran_id).update(
                        payment_details=json.dumps(data)
                    )

                    return Response("success", status=status.HTTP_200_OK)
                return Response("Payment Invalid", status=status.HTTP_400_BAD_REQUEST)


class IpnSslcommerze(views.APIView):

    def post(self, request):
        if request.data:
            data = orderVerify(request)
            if data["status"] == "VALID":
                tran_id = data["tran_id"]

                try:
                    consultancy_data = ConsultancyPayment.objects.filter(
                        tran_id=tran_id
                    ).values("userid", "consultancy_sheduleid")
                    consultancy_sheduleid = consultancy_data[0]["consultancy_sheduleid"]
                    ConsultancyTimeSchudile.objects.filter(
                        id=consultancy_sheduleid
                    ).update(is_consultancy_take=True)
                    UserConsultAppointmentRequest.objects.filter(
                        ConsultancyTimeSchudile=consultancy_sheduleid
                    ).update(payment_status=True)

                    ConsultancyPayment.objects.filter(Q(tran_id=tran_id)).update(
                        payment_details=json.dumps(data),
                    )
                    return Response("success", status=status.HTTP_200_OK)
                except Exception as e:
                    return Response("success call", status=status.HTTP_200_OK)


class Consultancy_Payment_success(views.APIView):
    def post(self, request):
        return Response("payment is success", status.HTTP_200_OK)


@api_view(["POST"])
def Consultancy_Payment_fail(request):
    return Response("Fail....", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def Consultancy_Payment_cancle(request):
    return Response("cancle", status=status.HTTP_200_OK)




class AppointmentSeeker_StarRating(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSeeker_StarRatingSerializer
    renderer_classes = [UserRenderer]
    lookup_field = "ConsultancyTimeSchudile"

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(
                Q(seekerid=user.userid) & Q(payment_status=True)
            )
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404


class ConsultantProvider_StarRating(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultantProvider_StarRatingSerializer
    renderer_classes = [UserRenderer]

    lookup_field = "ConsultancyTimeSchudile"

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(
                Q(ConsultancyTimeSchudile__consultancyid__userid=user.userid)
                & Q(payment_status=True)
            )
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404


class AppointmentSeeker_MissingAppointmentReason(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSeeker_MissingAppointmentReasonSerializer
    renderer_classes = [UserRenderer]

    lookup_field = "ConsultancyTimeSchudile"

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(
                Q(seekerid=user.userid) & Q(payment_status=True)
            )
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404


class GetSpecificCategoryServiceSearchData(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GetSpecificCategoryServiceSearchDataSerializer
    renderer_classes = [UserRenderer]

    def get_services(self, consultant_service_category, data):
        try:
            if consultant_service_category == "Education Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_consultant_service_locationcountry(
                    queryset, data["consultant_service_locationcountry"]
                )
                queryset = filterby_educationService_degree(
                    queryset, data["educationService_degree"]
                )
                queryset = filterby_consultant_servicebudget_startrange__gt(
                    queryset, data["consultant_servicebudget_startrange"]
                )
                queryset = filterby_consultant_servicebudget_endrange__lt(
                    queryset, data["consultant_servicebudget_endrange"]
                )
                return queryset

            if consultant_service_category == "Digital Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_digitalservice_type(
                    queryset, data["digitalservice_type"]
                )
                return queryset

            if consultant_service_category == "Immigration Consultancy Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_consultant_service_locationcountry(
                    queryset, data["consultant_service_locationcountry"]
                )
                queryset = filterby_consultant_servicebudget_startrange__gt(
                    queryset, data["consultant_servicebudget_startrange"]
                )
                queryset = filterby_consultant_servicebudget_endrange__lt(
                    queryset, data["consultant_servicebudget_endrange"]
                )
                return queryset

            if consultant_service_category == "Legal and Civil Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_consultant_service_locationcountry(
                    queryset, data["consultant_service_locationcountry"]
                )
                queryset = filterby_legalcivilservice_required(
                    queryset, data["legalcivilservice_required"]
                )
                queryset = filterby_legalcivilservice_issued(
                    queryset, data["legalcivilservice_issue"]
                )
                return queryset

            if consultant_service_category == "Medical Consultancy Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_consultant_service_locationcountry(
                    queryset, data["consultant_service_locationcountry"]
                )
                queryset = filterby_consultant_servicebudget_startrange__gt(
                    queryset, data["consultant_servicebudget_startrange"]
                )
                queryset = filterby_consultant_servicebudget_endrange__lt(
                    queryset, data["consultant_servicebudget_endrange"]
                )
                queryset = filterby_medicalconsultancyservice_treatment_area(
                    queryset, data["medicalconsultancyservice_treatment_area"]
                )
                return queryset

            if consultant_service_category == "Overseas Recruitment Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_consultant_service_locationcountry(
                    queryset, data["consultant_service_locationcountry"]
                )
                queryset = filterby_consultant_servicebudget_startrange__gt(
                    queryset, data["consultant_servicebudget_startrange"]
                )
                queryset = filterby_consultant_servicebudget_endrange__lt(
                    queryset, data["consultant_servicebudget_endrange"]
                )
                queryset = filterby_overseasrecruitmentservice_job_type(
                    queryset, data["overseasrecruitmentservice_job_type"]
                )
                return queryset

            if consultant_service_category == "Property Management Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_consultant_service_locationcountry(
                    queryset, data["consultant_service_locationcountry"]
                )
                queryset = filterby_propertymanagementservice_propertylocation(
                    queryset, data["propertymanagementservice_propertylocation"]
                )
                queryset = filterby_propertymanagementservice_type(
                    queryset, data["propertymanagementservice_type"]
                )
                queryset = filterby_propertymanagementservice_need(
                    queryset, data["propertymanagementservice_need"]
                )
                return queryset

            if consultant_service_category == "Tourism Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_tourismservices(queryset, data["tourismservices"])
                return queryset

            if consultant_service_category == "Trade Facilitation Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_consultant_service_locationcountry(
                    queryset, data["consultant_service_locationcountry"]
                )
                queryset = filterby_tradefacilitationservice_type(
                    queryset, data["tradefacilitationservice_type"]
                )
                queryset = filterby_tradefacilitationservice_Purpose(
                    queryset, data["tradefacilitationservice_Purpose"]
                )
                return queryset

            if consultant_service_category == "Training Service":
                queryset = filterby_consultant_service_category(
                    ConsultancyCreate, consultant_service_category
                )
                queryset = filterby_is_userconsultant_personal(
                    queryset, data["is_userconsultant_personal"]
                )
                queryset = filterby_is_userconsultant_company(
                    queryset, data["is_userconsultant_company"]
                )
                queryset = filterby_trainingservice_topic(
                    queryset, data["trainingservice_topic"]
                )
                queryset = filterby_trainingservice_duration(
                    queryset, data["trainingservice_duration"]
                )
                return queryset

        except User.DoesNotExist:
            raise Http404

    def post(self, request, service_Category):
        data = request.data
        consultancy = self.get_services(service_Category, data)

        serializer = self.serializer_class(consultancy, many=True)
        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)




class BecomeProUser(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def post(self, request):
        user = request.user
        if request.data["userid"] == user.userid:
            data = Pro_user_CREATE_and_GET_session(request, user)
            tran_id = data["post_body"]["tran_id"]

            if data["res"]["status"].lower() == "success":
                result = {}
                result["status"] = data["res"]["status"].lower()
                result["data"] = data["res"]["GatewayPageURL"]
                result["logo"] = data["res"]["storeLogo"]

                ProUserPayment.objects.create(userid=user, tran_id=tran_id)

                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(data["status"], status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class Pro_Payment_success(views.APIView):
    def post(self, request):

        tran_id = request.data["tran_id"]

        tran_id = ProUserPayment.objects.get(tran_id=tran_id)

        print("::::::::::::::::::::::::::::",tran_id)        

        

        # email_body = (
        #         "Hi "
        #         + "Probashi User \n"
        #         + " Congratulation , you become a pro user. \n"
        #         + "now you can create your own consultancy and get more clients. \n"
        #     )

        # data = {
        #     "email_body": email_body,
        #     "to_email": user_email,
        #     "email_subject": "Verify your email",
        # }

        # Util.send_email(data)


        return Response("success", status=status.HTTP_200_OK)


@api_view(["POST"])
def Pro_Payment_fail(request):
    return Response("Fail", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def Pro_Payment_cancle(request):
    return Response("cancle", status=status.HTTP_200_OK)


class ServiceSearchGetData(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        user = self.request.user
        if User.objects.filter(userid=user.userid).exists():
            location_data = set(
                ConsultancyCreate.objects.exclude(
                    consultant_service_locationcountry__isnull=True
                ).values_list("consultant_service_locationcountry", flat=True)
            )
            service_type = set(
                ConsultancyCreate.objects.exclude(
                    consultant_service_category__isnull=True
                ).values_list("consultant_service_category", flat=True)
            )

            context = {
                "success": True,
                "location_data": location_data,
                "service_type": service_type,
            }
            return Response(context, status=status.HTTP_200_OK)
        err_context = {"success": False, "message": "User not found"}
        return Response(err_context, status=status.HTTP_400_BAD_REQUEST)


class ServiceSearchFilterPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"


class ServiceSearchFilter(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ServiceSearchFilterSerializer
    renderer_classes = [UserRenderer]

    def get_service(self, data):

        location_data = data["location_data"]
        service_type = data["service_type"]

        queryset = ConsultancyCreate.objects.all()
        queryset = filterby_multiple_location(queryset, location_data)
        queryset = filterby_multiple_service(queryset, service_type)
        return queryset

    def post(self, request):
        user = self.request.user
        data = request.data
        search_user = self.get_service(data)
        serializer = self.serializer_class(search_user, many=True)
        paginator = ServiceSearchFilterPagination()
        page = paginator.paginate_queryset(serializer.data, request)
        if page is not None:
            return paginator.get_paginated_response(page)

        return Response(page, status=status.HTTP_200_OK)


class ServiceSearchField(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ServiceSearchFilterSerializer
    renderer_classes = [UserRenderer]

    def post(self, request):
        user = self.request.user
        data = request.data["service_field_data"]

        if c_user := ConsultancyCreate.objects.filter(
            Q(consultant_service_category__icontains=data)
            | Q(userid__user_fullname__icontains=data)
            | Q(userid__user_username__icontains=data)
        ):
            serializer = self.serializer_class(c_user, many=True)

            paginator = ServiceSearchFilterPagination()
            page = paginator.paginate_queryset(serializer.data, request)
            if page is not None:
                return paginator.get_paginated_response(page)

        else:
            data = []
            paginator = ServiceSearchFilterPagination()
            page = paginator.paginate_queryset(data, request)
            if page is not None:
                return paginator.get_paginated_response(page)

        return Response("Invalid Input", status=status.HTTP_400_BAD_REQUEST)


class SpecificServiceDescription(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    renderer_classes = [UserRenderer]

    def get(self, request, service_id):
        if consultancy_description := ConsultancyCreate.objects.filter(
            id=service_id
        ).values(
            "id",
            "consultant_service_category",
            "consultant_name",
            "consultant_service_locationcountry",
            "consultant_servicedescription",
            "userid__user_fullname",
        ):

            return Response(consultancy_description[0], status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)


class ConsultancyInfo(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get(self, request):
        consultancy_id = request.query_params.get("id")

        if consultancy := ConsultancyCreate.objects.filter(id=consultancy_id):
            context = {"success": True, "consultancy": consultancy.values().first()}
            return Response(context, status=status.HTTP_200_OK)
        err_context = {"success": False, "message": "invalid consultancy id"}
        return Response(
            err_context,
            status=status.HTTP_400_BAD_REQUEST,
        )




