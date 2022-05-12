from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework import permissions
from django.http import Http404
from yaml import serialize
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
)
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.db.models import Q
from auth_user_app.models import User
from itertools import chain


from probashi_backend.renderers import UserRenderer


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


# need to test in server...................................
class Consultancy_Payment_success(views.APIView):
    
    def post(self, request):
        tran_id = request.data["tran_id"]
        try:
            consultancy_data = ConsultancyPayment.objects.get(tran_id=tran_id)
            consultancy_sheduleid = consultancy_data.consultancy_sheduleid
            ConsultancyTimeSchudile.objects.filter(id=consultancy_sheduleid).update(
                is_consultancy_take=True
            )
            UserConsultAppointmentRequest.objects.filter(
                ConsultancyTimeSchudile=consultancy_sheduleid
            ).update(payment_status=True)

            ConsultancyPayment.objects.filter(Q(tran_id=tran_id)).update(
                val_id=request.data["val_id"],
                amount=request.data["amount"],
                card_type=request.data["card_type"],
                store_amount=request.data["store_amount"],
                card_no=request.data["card_no"],
                bank_tran_id=request.data["bank_tran_id"],
                status=request.data["status"],
                tran_date=request.data["tran_date"],
                error=request.data["error"],
                currency=request.data["currency"],
                card_issuer=request.data["card_issuer"],
                card_brand=request.data["card_brand"],
                card_sub_brand=request.data["card_sub_brand"],
                card_issuer_country=request.data["card_issuer_country"],
                card_issuer_country_code=request.data["card_issuer_country_code"],
                store_id=request.data["store_id"],
                verify_sign=request.data["verify_sign"],
                verify_key=request.data["verify_key"],
                verify_sign_sha2=request.data["verify_sign_sha2"],
                currency_type=request.data["currency_type"],
                currency_amount=request.data["currency_amount"],
                currency_rate=request.data["currency_rate"],
                base_fair=request.data["base_fair"],
                value_a=request.data["value_a"],
                value_b=request.data["value_b"],
                value_c=request.data["value_c"],
                value_d=request.data["value_d"],
                subscription_id=request.data["subscription_id"],
                risk_level=request.data["risk_level"],
                risk_title=request.data["risk_title"],
            )
            return Response("success", status=status.HTTP_200_OK)
        except:
            return Response("fail", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def Consultancy_Payment_fail(request):

    return Response("Fail", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def Consultancy_Payment_cancle(request):
    # print('::::::::::::::::::',request.data)
    return Response("cancle", status=status.HTTP_200_OK)


# ----------------------------------------x---------------------------------------x--------------------------


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

                consultant_service_locationcountry = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_service_locationcountry=data[
                            "consultant_service_locationcountry"
                        ]
                    )
                )
                educationService_degree = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(educationService_degree=data["educationService_degree"])
                )
                consultant_servicebudget_startrange = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_servicebudget_startrange__gt=data[
                            "consultant_servicebudget_startrange"
                        ]
                    )
                )
                consultant_servicebudget_endrange = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_servicebudget_endrange__lt=data[
                            "consultant_servicebudget_endrange"
                        ]
                    )
                )
                search = [
                    consultant_service_locationcountry,
                    educationService_degree,
                    consultant_servicebudget_startrange,
                    consultant_servicebudget_endrange,
                ]

                count = 1
                search_data = consultant_service_locationcountry
                for i, d in zip(search, data):
                    # print(count, '::::::::i:::::::::::',type(i),data[d])
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data


            if consultant_service_category == "Digital Service":

                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )

                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )
                digitalservice_type = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(digitalservice_type=data["digitalservice_type"])
                )

                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    digitalservice_type,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

            if consultant_service_category == "Immigration Consultancy Service":

                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )
                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )

                consultant_service_locationcountry = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_service_locationcountry=data[
                            "consultant_service_locationcountry"
                        ]
                    )
                )
                consultant_servicebudget_startrange__gt = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            consultant_servicebudget_startrange__gt=data[
                                "consultant_servicebudget_startrange"
                            ]
                        )
                    )
                )
                consultant_servicebudget_endrange__lt = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            consultant_servicebudget_endrange__lt=data[
                                "consultant_servicebudget_endrange"
                            ]
                        )
                    )
                )
                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    consultant_service_locationcountry,
                    consultant_servicebudget_startrange__gt,
                    consultant_servicebudget_endrange__lt,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i
                return search_data

            if consultant_service_category == "Legal and Civil Service":

                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )

                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )
                consultant_service_locationcountry = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_service_locationcountry=data[
                            "consultant_service_locationcountry"
                        ]
                    )
                )
                legalcivilservice_required = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(legalcivilservice_required=data["legalcivilservice_required"])
                )
                legalcivilservice_issue = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(legalcivilservice_issue=data["legalcivilservice_issue"])
                )

                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    consultant_service_locationcountry,
                    legalcivilservice_required,
                    legalcivilservice_issue,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

            if consultant_service_category == "Medical Consultancy Service":

                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )
                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )
                consultant_service_locationcountry = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_service_locationcountry=data[
                            "consultant_service_locationcountry"
                        ]
                    )
                )
                consultant_servicebudget_startrange__gt = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            consultant_servicebudget_startrange__gt=data[
                                "consultant_servicebudget_startrange"
                            ]
                        )
                    )
                )
                consultant_servicebudget_endrange__lt = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            consultant_servicebudget_endrange__lt=data[
                                "consultant_servicebudget_endrange"
                            ]
                        )
                    )
                )
                medicalconsultancyservice_treatment_area = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            medicalconsultancyservice_treatment_area=data[
                                "medicalconsultancyservice_treatment_area"
                            ]
                        )
                    )
                )

                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    consultant_service_locationcountry,
                    medicalconsultancyservice_treatment_area,
                    consultant_servicebudget_startrange__gt,
                    consultant_servicebudget_endrange__lt,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

            if consultant_service_category == "Overseas Recruitment Service":

                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )
                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )
                consultant_service_locationcountry = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_service_locationcountry=data[
                            "consultant_service_locationcountry"
                        ]
                    )
                )
                consultant_servicebudget_startrange__gt = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            consultant_servicebudget_startrange__gt=data[
                                "consultant_servicebudget_startrange"
                            ]
                        )
                    )
                )
                consultant_servicebudget_endrange__lt = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            consultant_servicebudget_endrange__lt=data[
                                "consultant_servicebudget_endrange"
                            ]
                        )
                    )
                )
                overseasrecruitmentservice_job_type = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        overseasrecruitmentservice_job_type=data[
                            "overseasrecruitmentservice_job_type"
                        ]
                    )
                )

                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    consultant_service_locationcountry,
                    overseasrecruitmentservice_job_type,
                    consultant_servicebudget_startrange__gt,
                    consultant_servicebudget_endrange__lt,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

            if consultant_service_category == "Property Management Service":

                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )
                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )
                consultant_service_locationcountry = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_service_locationcountry=data[
                            "consultant_service_locationcountry"
                        ]
                    )
                )
                propertymanagementservice_propertylocation = (
                    ConsultancyCreate.objects.filter(
                        Q(consultant_service_category=consultant_service_category)
                        & Q(
                            propertymanagementservice_propertylocation=data[
                                "propertymanagementservice_propertylocation"
                            ]
                        )
                    )
                )
                propertymanagementservice_type = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        propertymanagementservice_type=data[
                            "propertymanagementservice_type"
                        ]
                    )
                )
                propertymanagementservice_need = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        propertymanagementservice_need=data[
                            "propertymanagementservice_need"
                        ]
                    )
                )
                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    consultant_service_locationcountry,
                    propertymanagementservice_propertylocation,
                    propertymanagementservice_type,
                    propertymanagementservice_need,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

            if consultant_service_category == "Tourism Service":
                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )
                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )
                tourismservices = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(tourismservices=data["tourismservices"])
                )

                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    tourismservices,
                ]
                count = 1
                search_data = both
                for i, d in zip(search, data):
                    # print(count, '::::::::i:::::::::::',type(i),data[d])
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

            if consultant_service_category == "Trade Facilitation Service":
                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )
                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )
                consultant_service_locationcountry = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        consultant_service_locationcountry=data[
                            "consultant_service_locationcountry"
                        ]
                    )
                )
                tradefacilitationservice_type = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        tradefacilitationservice_type=data[
                            "tradefacilitationservice_type"
                        ]
                    )
                )
                tradefacilitationservice_Purpose = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(
                        tradefacilitationservice_Purpose=data[
                            "tradefacilitationservice_Purpose"
                        ]
                    )
                )

                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    consultant_service_locationcountry,
                    tradefacilitationservice_type,
                    tradefacilitationservice_Purpose,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1
                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

            if consultant_service_category == "Training Service":

                both = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (
                        Q(is_userconsultant_personal=data["is_userconsultant_personal"])
                        | Q(is_userconsultant_company=data["is_userconsultant_company"])
                    )
                )
                is_userconsultant_personal = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & (Q(is_userconsultant_personal=data["is_userconsultant_personal"]))
                )
                is_userconsultant_company = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(is_userconsultant_company=data["is_userconsultant_company"])
                )

                trainingservice_topic = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(trainingservice_topic=data["trainingservice_topic"])
                )

                trainingservice_duration = ConsultancyCreate.objects.filter(
                    Q(consultant_service_category=consultant_service_category)
                    & Q(trainingservice_duration=data["trainingservice_duration"])
                )

                search = [
                    is_userconsultant_personal,
                    is_userconsultant_company,
                    trainingservice_topic,
                    trainingservice_duration,
                ]

                count = 1
                search_data = both
                for i, d in zip(search, data):
                    if data[d] == "" or data[d] == []:
                        pass
                    else:
                        count += 1

                        if count > 1:
                            search_data &= i
                        else:
                            search_data = i

                return search_data

        except User.DoesNotExist:
            raise Http404

    def post(self, request, service_Category):
        data = request.data
        consultancy = self.get_services(service_Category, data)

        serializer = self.serializer_class(
            consultancy, many=True
        )
        data = {"data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)


# ------------------------------------------------- pro user payment start------------------------------------------------------


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
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tran_id = request.data["tran_id"]
        
        if ProUserPayment.objects.filter(tran_id=tran_id).exists():
            pro_user = ProUserPayment.objects.filter(tran_id=tran_id).values("userid")[
                0
            ]["userid"]
            User.objects.filter(userid=pro_user).update(is_pro_user=True)

            ProUserPayment.objects.filter(tran_id=tran_id).update(
                val_id=request.data["val_id"],
                amount=request.data["amount"],
                card_type=request.data["card_type"],
                store_amount=request.data["store_amount"],
                card_no=request.data["card_no"],
                bank_tran_id=request.data["bank_tran_id"],
                status=request.data["status"],
                tran_date=request.data["tran_date"],
                error=request.data["error"],
                currency=request.data["currency"],
                card_issuer=request.data["card_issuer"],
                card_brand=request.data["card_brand"],
                card_sub_brand=request.data["card_sub_brand"],
                card_issuer_country=request.data["card_issuer_country"],
                card_issuer_country_code=request.data["card_issuer_country_code"],
                store_id=request.data["store_id"],
                verify_sign=request.data["verify_sign"],
                verify_key=request.data["verify_key"],
                verify_sign_sha2=request.data["verify_sign_sha2"],
                currency_type=request.data["currency_type"],
                currency_amount=request.data["currency_amount"],
                currency_rate=request.data["currency_rate"],
                base_fair=request.data["base_fair"],
                value_a=request.data["value_a"],
                value_b=request.data["value_b"],
                value_c=request.data["value_c"],
                value_d=request.data["value_d"],
                subscription_id=request.data["subscription_id"],
                risk_level=request.data["risk_level"],
                risk_title=request.data["risk_title"],
            )
        return Response("success", status=status.HTTP_200_OK)


@api_view(["POST"])
def Pro_Payment_fail(request):
    # print("::::::::::::::::::", request.data)

    return Response("Fail", status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def Pro_Payment_cancle(request):
    # print("::::::::::::::::::", request.data)
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

        location_data_search_data = ConsultancyCreate.objects.filter(
            consultant_service_locationcountry__in=location_data
        )

        service_type_search_data = ConsultancyCreate.objects.filter(
            consultant_service_category__in=service_type
        )

        if location_data != [] and service_type != []:
            search = location_data_search_data & service_type_search_data
        elif location_data != [] and service_type == []:
            search = location_data_search_data
        elif location_data == [] and service_type != []:
            search = service_type_search_data

        else:
            search = ConsultancyCreate.objects.all()

        return search

    def post(self, request):
        user = self.request.user
        data = request.data
        search_user = self.get_service(data)

        serializer = self.serializer_class(search_user, many=True)

        # context = {"success":True,"data":details}
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
