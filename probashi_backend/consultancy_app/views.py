from cgitb import lookup
from multiprocessing import context
from urllib import request, response
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import (ConsultancyCreate, 
                    UserConsultAppointmentRequest,
                    ConsultancyTimeSchudile)
from .serializers import (ConsultancyCreateSerializer, ServiceCategorySerializer,
                        ConsultancyTimeSchudileSerializer,
                        GetAllServicesCategoryScheduleSerializer,
                        GetAllCategoryNotTakingScheduleSerializer,

                        ConsultantAppointmentRequestSerializer, 
                        AppointmentSeeker_StarRatingSerializer,
                        ConsultantProvider_StarRatingSerializer, 
                        AppointmentSeeker_MissingAppointmentReasonSerializer,
                        GetServicesSpecificCategorySerializer,
                        GetSpecificCategoryServiceSearchDataSerializer,
                        
                        )
from . sslcommerz_helper import (Pro_user_CREATE_and_GET_session ,ipn_orderverify, 
                                Consultancy_CREATE_and_GET_session)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.db.models import Q
from auth_user_app.models import User



# class GetAllServiceSetPagination(PageNumberPagination):
#     page_size = 20
#     # page_size_query_param = 'services'
#     max_page_size = 10000

class GetAllServicesCategoryView(generics.ListAPIView):
    # queryset = ConsultancyCreate.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    # pagination_class = GetAllServiceSetPagination

    def get_queryset(self):
        queryset = ConsultancyCreate.objects.annotate().values('consultant_service_category').distinct()
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ServiceCategorySerializer(queryset, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)



class GetSpecificCategoriesServiceSetPagination(PageNumberPagination):
    page_size = 2
    # page_number = 1
    page_size_query_param = 'page_size'
    max_page_size = 10000

    
class GetServicesSpecificCategoryData(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = GetSpecificCategoriesServiceSetPagination

    def get_services(self,consultant_service_category):
        try:
            return ConsultancyCreate.objects.filter(consultant_service_category__exact=consultant_service_category)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, consultant_service_category, format=None):
        queryset = self.get_services(consultant_service_category)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = GetServicesSpecificCategorySerializer(page, many=True)
        data = {'data' : paginator.get_paginated_response(serializer.data)}
        return data


# ----------------------------x---------------------------x---------------
class ConsultancyCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = ConsultancyCreate.objects.all()
    serializer_class = ConsultancyCreateSerializer

    def create(self, request):
        user = request.user
        if request.data['userid'] == user.userid:
            serializer = ConsultancyCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Json Serializer Error", status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)



# ----------------------------x---------------------------x---------------


class ConsultancyTimeSchudileView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultancyTimeSchudileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ConsultancyTimeSchudile.objects.filter(consultancyid__userid=user.userid)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConsultancyTimeSchudileSerializer(queryset, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)



class GetAllServicesCategorySchedule(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = GetAllServicesCategoryScheduleSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = ConsultancyCreate.objects.filter(userid=user.userid)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetAllServicesCategoryScheduleSerializer(queryset, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)




class NotTakingScheduil_forEachService(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,service_Category):
        try:
            return ConsultancyCreate.objects.filter(Q(consultant_service_category = service_Category ) )
        except ConsultancyCreate.DoesNotExist:
            raise Http404

    def get(self,request,service_Category):
        consultancy = self.get_object(service_Category)

        serializer = GetAllCategoryNotTakingScheduleSerializer(consultancy, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)




# ######################## need to be added payment work........................................

class AppointmentSeeker_ConsultantRequest(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):

        # work with payment gateway 
            # after complete payment then execute billow code


        # user = self.request.user
        # print(request.data['seekerid'] == user.userid)
        # if request.data['seekerid'] == user.userid:
        #     serializer = ConsultantAppointmentRequestSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         ConsultancyTimeSchudile.objects.filter(id=request.data['ConsultancyTimeSchudile']).update(is_consultancy_take=True)
        #         # print("::::::::::::",serializer.data)
        #         return Response(serializer.data, status=status.HTTP_200_OK)
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({"message": "You are not authorized to make this request"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        user = request.user
        if request.data['seekerid'] == user.userid:
            data = Consultancy_CREATE_and_GET_session(request, user)
            print(":::::::", data)

            result = {}
            result['status'] = data['status'].lower()
            result['data'] = data['GatewayPageURL']
            result['logo'] = data['storeLogo']

            return Response(result, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)








class AppointmentSeeker_StarRating(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = UserConsultAppointmentRequest.objects.all()
    serializer_class = AppointmentSeeker_StarRatingSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(seekerid=user.userid)
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404


class ConsultantProvider_StarRating(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultantProvider_StarRatingSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(consultancy_id__userid=user.userid)
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404




class AppointmentSeeker_MissingAppointmentReason(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppointmentSeeker_MissingAppointmentReasonSerializer
    lookup_field = 'id'

    def get_queryset(self):
        try:
            user = self.request.user
            return UserConsultAppointmentRequest.objects.filter(seekerid=user)
        except UserConsultAppointmentRequest.DoesNotExist:
            raise Http404




# Need to be work..........................................................

'''
"Education Service:
    Country [ok],   "educationService_degree" [sub],  Budget [ok]"
"Overseas Recruitment Service:
    Provider_type  [ok],  Region [no_need], Country [ok], "overseasrecruitmentservice_jobtype"  [sub], Budget [ok] "
"Immigration Consultancy Service:
    Provider_type  [ok], Country [ok], Budget [ok]"
"Medical Consultancy Service:
    Provider_type  [ok],  Country [ok], "medicalconsultancyservice_treatment-area" [sub], Budget [ok]"
"Legal&Civil Service:
    Provider_type  [ok], Country  [ok], "legalcivilservice_required" [sub], "legalcivilservice_issue" [sub2]"
"Property Management Service:
    Provider_type  [ok], Country  [ok], district [sub3], "propertymanagementservice_type [sub]", "propertymanagementservice_need" [sub2]"
"Tourism Service:
    Provider_type  [ok], "tourismservices [sub]"
"Training Service:
    Provider_type  [ok], "trainingservice_topic" [sub], "trainingservice_duration" [sub2]"
"Digital Service:
    Provider_type  [ok], "digitalservice_type" [sub]"
"Trade Facilitation Service:
    Provider_type  [ok], Country [ok], "tradefacilitationservice_type"  [sub], tradefacilitationservice_Purpose  [sub2]"

'''





class GetSpecificCategoryServiceSearchData(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_services(self,consultant_service_category, data):
        try:
            if consultant_service_category == 'Education Service':
                # print(":::::::::::", data['consultant_service_locationcountry'])
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                        Q(educationService_degree = data['educationService_degree']) &
                                                        Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                        Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
            if consultant_service_category == 'Digital Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) &
                                                        Q(digitalservice_type = data['digitalservice_type']) )
            if consultant_service_category == 'Immigration Consultancy Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                        Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                        Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                        Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
            if consultant_service_category == 'Legal&Civil Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                        Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                        Q(legalcivilservice_required = data['legalcivilservice_required']) &
                                                        Q(legalcivilservice_issue = data['legalcivilservice_issue']) )
            if consultant_service_category == 'Medical Consultancy Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                        Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                        Q(medicalconsultancyservice_treatment_area = data['medicalconsultancyservice_treatment_area']) &
                                                        Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                        Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
            if consultant_service_category == 'Overseas Recruitment Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                        Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                        Q(overseasrecruitmentservice_job_type = data['overseasrecruitmentservice_job_type']) &
                                                        Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                        Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']))

            if consultant_service_category == 'Property Management Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                        Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                        Q(propertymanagementservice_propertylocation= data['propertymanagementservice_propertylocation']) &
                                                        Q(propertymanagementservice_type = data['propertymanagementservice_type']) &
                                                        Q(propertymanagementservice_need= data['propertymanagementservice_need']) )
            if consultant_service_category == 'Tourism Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                        Q(tourismservices = data['tourismservices']) )
            if consultant_service_category == 'Trade Facilitation Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category )  &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                        Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                        Q(tradefacilitationservice_type = data['tradefacilitationservice_type']) &
                                                        Q(tradefacilitationservice_Purpose = data['tradefacilitationservice_Purpose']) )
            if consultant_service_category == 'Training Service':
                return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                        (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                        Q(is_userconsultant_company = data['is_userconsultant_company'])) &
                                                        Q(trainingservice_topic = data['trainingservice_topic']) &
                                                        Q(trainingservice_duration = data['trainingservice_duration']) )
        except User.DoesNotExist:
            raise Http404


    def post(self,request,service_Category):
        data = request.data
        consultancy = self.get_services(service_Category,data)

        serializer = GetSpecificCategoryServiceSearchDataSerializer(consultancy, many=True)
        return Response(serializer.data)





# ------------------------------------------------- pro user payment start------------------------------------------------------

class BecomeProUser(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        user = request.user
        if request.data['userid'] == user.userid:
            data = Pro_user_CREATE_and_GET_session(request, user)
            # print(":::::::", data)

            result = {}
            result['status'] = data['status'].lower()
            result['data'] = data['GatewayPageURL']
            result['logo'] = data['storeLogo']

            return Response(result, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class ValidityWithIPN(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        print("ipn data::::::",request.data)
        if request.data:
            data = ipn_orderverify(request)
            print("ipn data::::::",data)
            return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
# ------------------------------------------------- pro user payment end------------------------------------------------------

@api_view(['POST'])
def payment_success(request):
    return Response("success", status=status.HTTP_200_OK)


@api_view(['POST'])
def payment_fail(request):
    return Response("Fail", status=status.HTTP_200_OK)

@api_view(['POST'])
def payment_cancle(request):
    return Response("cancle", status=status.HTTP_200_OK)

