from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import (ConsultancyCreate, 
                    UserConsultAppointmentRequest,
                    ConsultancyTimeSchudile,
                    ProUserPayment,
                    ConsultancyPayment)

from .serializers import (ConsultancyCreateSerializer, ServiceCategorySerializer,
                        ConsultancyTimeSchudileSerializer,
                        GetAllServicesCategoryScheduleSerializer,
                        GetAllCategoryNotTakingScheduleSerializer,
                        GetAllCategoryScheduleSerializer,
                        ConsultantAppointmentRequestSerializer, 
                        AppointmentSeeker_StarRatingSerializer,
                        ConsultantProvider_StarRatingSerializer, 
                        AppointmentSeeker_MissingAppointmentReasonSerializer,
                        GetServicesSpecificCategorySerializer,
                        GetSpecificCategoryServiceSearchDataSerializer,
                        ConsultancyPaymentSerializer,
                        )
from . sslcommerz_helper import (Pro_user_CREATE_and_GET_session ,
                                Consultancy_CREATE_and_GET_session)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from django.db.models import Q
from auth_user_app.models import User


from probashi_backend.renderers import UserRenderer


# class GetAllServiceSetPagination(PageNumberPagination):
#     page_size = 20
#     # page_size_query_param = 'services'
#     max_page_size = 10000

class GetAllServicesCategoryView(generics.ListAPIView):
    # queryset = ConsultancyCreate.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

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
    renderer_classes = [UserRenderer]


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
    renderer_classes = [UserRenderer]


    def create(self, request):
        print("permission class::::::::::::::::::", self.permission_classes)
        user = request.user
        if request.data['userid'] == user.userid:
            serializer = ConsultancyCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)



# ----------------------------x---------------------------x---------------

class ConsultancyTimeSchudileView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConsultancyTimeSchudileSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        user = self.request.user
        queryset = ConsultancyTimeSchudile.objects.filter(consultancyid__userid=user.userid)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConsultancyTimeSchudileSerializer(queryset, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        user = request.user
        con_user = ConsultancyTimeSchudile.objects.filter(Q(consultancyid__userid=user.userid)).exists()
        # print("con_user::::::::::::::::::", con_user)   
        if con_user == True:
            serializer = ConsultancyTimeSchudileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "You are not authorized to perform this action"}, status=status.HTTP_400_BAD_REQUEST)




class GetAllServicesCategorySchedule(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = GetAllServicesCategoryScheduleSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        user = self.request.user

        queryset = ConsultancyCreate.objects.filter(userid=user.userid)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetAllServicesCategoryScheduleSerializer(queryset, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)




class SpecificServicesSchedules(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = GetAllServicesCategoryScheduleSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self,id):
        id = id
        # print('id::::::::',id)
        queryset = ConsultancyCreate.objects.filter(Q(id=id))
        return queryset

    def list(self, request):
        # print(":::::::::::::::::", request.query_params.get("id"))
        id = request.query_params.get("id")
        queryset = self.get_queryset(id)
        serializer = GetAllServicesCategoryScheduleSerializer(queryset, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)






class ALLScheduils_forConsultancyProvider(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_object(self, user_id):
        try:
            return ConsultancyCreate.objects.filter(Q(userid=user_id))
        except ConsultancyCreate.DoesNotExist:
            raise Http404

    def get(self,request):
        user_id = request.user.userid
        
        consultancy = self.get_object(user_id)

        serializer = GetAllCategoryScheduleSerializer(consultancy, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)












class NotTakingScheduil_forSpecificUser(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def get_object(self, user_id):
        try:
            # print('::::::::::::::::::', ConsultancyTimeSchudile.objects.filter(Q(consultancyid__userid=user_id)))
            return ConsultancyCreate.objects.filter(Q(userid=user_id))
        except ConsultancyCreate.DoesNotExist:
            raise Http404

    def get(self,request):
        user_id = request.query_params.get('user_id')
        # user_id = self.request.user.userid
        # print(':::::::::::::',user)
        consultancy = self.get_object(user_id)

        serializer = GetAllCategoryNotTakingScheduleSerializer(consultancy, many=True)
        data = {'data' : serializer.data}
        return Response(data, status=status.HTTP_200_OK)




# ######################## need to be added payment work........................................

#################################need to be complete payment............

class AppointmentSeeker_ConsultantRequest(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [UserRenderer]

    def post(self, request):
        
        user = request.user
        # print(":::::::::::", user.userid)
        consultancyTimeSchudile= ConsultancyTimeSchudile.objects.filter(id=request.data['ConsultancyTimeSchudile']).first()
        print(":::::::::::", consultancyTimeSchudile)
        if request.data['seekerid'] == user.userid and consultancyTimeSchudile != None:
            data = Consultancy_CREATE_and_GET_session(request, user)
            # print("status:::::::", data['res']['status'].lower())
            tran_id = data['post_body']['tran_id']
            
            if data['res']['status'].lower() == 'success':
                result = {}
                result['status'] = data['res']['status'].lower()
                result['data'] = data['res']['GatewayPageURL']
                result['logo'] = data['res']['storeLogo']

                consultancy_paydata = {'userid': user.userid,'consultancy_sheduleid':request.data['ConsultancyTimeSchudile'] ,'tran_id': tran_id}
                serializer = ConsultancyPaymentSerializer(data=consultancy_paydata)
                if serializer.is_valid():
                    serializer.save()

                    
                    serializer = ConsultantAppointmentRequestSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()

                        #########work in success URL
                        # ConsultancyTimeSchudile.objects.filter(id=request.data['ConsultancyTimeSchudile']).update(is_consultancy_take=True)
                        # print("::::::::::::",serializer.data)
                        # success_msg = {'success': True, 'data' : result}
                        return Response(result, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "You are not authorized to make this request"}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response(data['res']['status'].lower(), status=status.HTTP_400_BAD_REQUEST)
        error_msg = {'success': False, 'message': 'seekerid or ConsultancyTimeSchudile invalid'}
        return Response('seekerid or ConsultancyTimeSchudile invalid',status=status.HTTP_400_BAD_REQUEST)







class Consultancy_Payment_success(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tran_id = request.data['tran_id']
        # print('::::::::::::::::::',tran_id)
        # print('::::::::::::::::::',request.data)


        if ConsultancyPayment.objects.filter(tran_id=tran_id).exists():
            consultancy_data = ConsultancyPayment.objects.filter(tran_id=tran_id).values('userid','consultancy_sheduleid')
            consultancy_sheduleid = consultancy_data[0]['consultancy_sheduleid']
            # print('consultancy::::::::::::::::::',consultancy_sheduleid)
            ConsultancyTimeSchudile.objects.filter(id=consultancy_sheduleid).update(is_consultancy_take=True)
            UserConsultAppointmentRequest.objects.filter(ConsultancyTimeSchudile=consultancy_sheduleid).update(payment_status=True)

            
            ConsultancyPayment.objects.filter(Q(tran_id=tran_id)).update(
                val_id=request.data['val_id'],
                amount = request.data['amount'],
                card_type = request.data['card_type'],
                store_amount = request.data['store_amount'],
                card_no = request.data['card_no'],
                bank_tran_id = request.data['bank_tran_id'],
                status = request.data['status'],
                tran_date = request.data['tran_date'],
                error = request.data['error'],
                currency = request.data['currency'],
                card_issuer = request.data['card_issuer'],
                card_brand = request.data['card_brand'],
                card_sub_brand = request.data['card_sub_brand'],
                card_issuer_country = request.data['card_issuer_country'],
                card_issuer_country_code = request.data['card_issuer_country_code'],
                store_id = request.data['store_id'],
                verify_sign = request.data['verify_sign'],
                verify_key = request.data['verify_key'],
                verify_sign_sha2 = request.data['verify_sign_sha2'],
                currency_type = request.data['currency_type'],
                currency_amount = request.data['currency_amount'],
                currency_rate = request.data['currency_rate'],
                base_fair = request.data['base_fair'],
                value_a = request.data['value_a'],
                value_b = request.data['value_b'],
                value_c = request.data['value_c'],
                value_d = request.data['value_d'],
                subscription_id = request.data['subscription_id'],
                risk_level = request.data['risk_level'],
                risk_title = request.data['risk_title']
            )
        return Response("success", status=status.HTTP_200_OK)


@api_view(['POST'])
def Consultancy_Payment_fail(request):
    # print('::::::::::::::::::',request.data)
    
    return Response("Fail", status=status.HTTP_200_OK)

@api_view(['POST'])
def Consultancy_Payment_cancle(request):
    # print('::::::::::::::::::',request.data)
    return Response("cancle", status=status.HTTP_200_OK)






# ----------------------------------------x---------------------------------------x--------------------------




class AppointmentSeeker_StarRating(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = UserConsultAppointmentRequest.objects.all()
    serializer_class = AppointmentSeeker_StarRatingSerializer
    renderer_classes = [UserRenderer]

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
    renderer_classes = [UserRenderer]

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
    renderer_classes = [UserRenderer]

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
    # renderer_classes = [UserRenderer]


    def get_services(self,consultant_service_category, data):
        try:
            if consultant_service_category == 'Education Service':
                print("EDU:::::::::::", type(data['consultant_service_locationcountry']))
                if data['educationService_degree'] != [] and data['consultant_service_locationcountry'] != '':
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(educationService_degree = data['educationService_degree']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                elif data['educationService_degree'] == [] and data['consultant_service_locationcountry'] != '':
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                elif data['consultant_service_locationcountry'] == '' and data['educationService_degree'] != []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            Q(educationService_degree = data['educationService_degree']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                else:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )                                            
            
            
            if consultant_service_category == 'Digital Service':
                if data['digitalservice_type'] != []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) &
                                                            Q(digitalservice_type = data['digitalservice_type']) )
                else:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) )
            
            
            if consultant_service_category == 'Immigration Consultancy Service':
                
                if data['consultant_service_locationcountry'] != '':
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                else:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
            

            
            if consultant_service_category == 'Legal and Civil Service':
                
                if data['consultant_service_locationcountry'] != '' and data['legalcivilservice_required'] != [] and data['legalcivilservice_issue'] != [] :
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(legalcivilservice_required = data['legalcivilservice_required']) &
                                                            Q(legalcivilservice_issue = data['legalcivilservice_issue']) )

                elif data['consultant_service_locationcountry'] == '' and data['legalcivilservice_required'] != [] and data['legalcivilservice_issue'] != [] :
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(legalcivilservice_required = data['legalcivilservice_required']) &
                                                            Q(legalcivilservice_issue = data['legalcivilservice_issue']) ))

                elif data['consultant_service_locationcountry'] != '' and data['legalcivilservice_required'] == [] and data['legalcivilservice_issue'] != [] :
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(legalcivilservice_issue = data['legalcivilservice_issue']) )

                elif data['consultant_service_locationcountry'] != '' and data['legalcivilservice_required'] != [] and data['legalcivilservice_issue'] == []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(legalcivilservice_required = data['legalcivilservice_required']) )

                elif data['consultant_service_locationcountry'] == '' and data['legalcivilservice_required'] == [] and data['legalcivilservice_issue'] != []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(legalcivilservice_issue = data['legalcivilservice_issue']) )

                elif data['consultant_service_locationcountry'] != '' and data['legalcivilservice_required'] == [] and data['legalcivilservice_issue'] == []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) )

                elif data['consultant_service_locationcountry'] == '' and data['legalcivilservice_required'] != [] and data['legalcivilservice_issue'] == [] :
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(legalcivilservice_required = data['legalcivilservice_required']) )
                else:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])))


            
            
            if consultant_service_category == 'Medical Consultancy Service':
                if data['consultant_service_locationcountry'] != '' and data['medicalconsultancyservice_treatment_area'] != []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(medicalconsultancyservice_treatment_area = data['medicalconsultancyservice_treatment_area']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                elif data['consultant_service_locationcountry'] == '' and data['medicalconsultancyservice_treatment_area'] != []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(medicalconsultancyservice_treatment_area = data['medicalconsultancyservice_treatment_area']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                elif data['consultant_service_locationcountry'] != '' and data['medicalconsultancyservice_treatment_area'] == []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                else: 
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']) )
                
            
            
            if consultant_service_category == 'Overseas Recruitment Service':
                if data['consultant_service_locationcountry'] != '' and data['overseasrecruitmentservice_job_type'] != []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(overseasrecruitmentservice_job_type = data['overseasrecruitmentservice_job_type']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']))
                elif data['consultant_service_locationcountry'] == '' and data['overseasrecruitmentservice_job_type'] != []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(overseasrecruitmentservice_job_type = data['overseasrecruitmentservice_job_type']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']))

                elif data['consultant_service_locationcountry'] != '' and data['overseasrecruitmentservice_job_type'] == []:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_service_locationcountry= data['consultant_service_locationcountry']) &
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']))

                else:
                    return ConsultancyCreate.objects.filter(Q(consultant_service_category = consultant_service_category ) &
                                                            (Q(is_userconsultant_personal = data['is_userconsultant_personal']) |
                                                            Q(is_userconsultant_company = data['is_userconsultant_company'])) & 
                                                            Q(consultant_servicebudget_startrange__gt = data['consultant_servicebudget_startrange']) &
                                                            Q(consultant_servicebudget_endrange__lt = data['consultant_servicebudget_endrange']))

                
            

# ============================================================================================================
            
            if consultant_service_category == 'Property Management Service':
                if (data['consultant_service_locationcountry'] != '' and data['propertymanagementservice_propertylocation'] != '' and  
                        data['propertymanagementservice_type'] != [] and data['propertymanagementservice_need'] != []):
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
        # data = {'data': serializer.data}
        return Response(serializer.data, status=status.HTTP_200_OK)





# ------------------------------------------------- pro user payment start------------------------------------------------------

class BecomeProUser(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def post(self,request):
        user = request.user
        if request.data['userid'] == user.userid:
            data = Pro_user_CREATE_and_GET_session(request, user)
            # print(":::::::", data['post_body']['tran_id'])
            tran_id = data['post_body']['tran_id']

            if data['res']['status'].lower() == 'success':
                result = {}
                result['status'] = data['res']['status'].lower()
                result['data'] = data['res']['GatewayPageURL']
                result['logo'] = data['res']['storeLogo']

                ProUserPayment.objects.create(userid=user,tran_id=tran_id)

                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response(data['status'], status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# class ValidityWithIPN(views.APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def post(self,request):
#         print("ipn data::::::",request.data)
#         if request.data:
#             data = ipn_orderverify(request)
#             print("ipn data::::::",data)
#             return Response(data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)
        
# ------------------------------------------------- pro user payment end------------------------------------------------------

class Pro_Payment_success(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tran_id = request.data['tran_id']
        # print('::::::::::::::::::',tran_id)
        # print('::::::::::::::::::',request.data)
        if ProUserPayment.objects.filter(tran_id=tran_id).exists():
            pro_user = ProUserPayment.objects.filter(tran_id=tran_id).values('userid')[0]['userid']
            # print('::::::::::::::::::',pro_user)
            User.objects.filter(userid=pro_user).update(is_pro_user=True)
            
            ProUserPayment.objects.filter(tran_id=tran_id).update(
                val_id=request.data['val_id'],
                amount = request.data['amount'],
                card_type = request.data['card_type'],
                store_amount = request.data['store_amount'],
                card_no = request.data['card_no'],
                bank_tran_id = request.data['bank_tran_id'],
                status = request.data['status'],
                tran_date = request.data['tran_date'],
                error = request.data['error'],
                currency = request.data['currency'],
                card_issuer = request.data['card_issuer'],
                card_brand = request.data['card_brand'],
                card_sub_brand = request.data['card_sub_brand'],
                card_issuer_country = request.data['card_issuer_country'],
                card_issuer_country_code = request.data['card_issuer_country_code'],
                store_id = request.data['store_id'],
                verify_sign = request.data['verify_sign'],
                verify_key = request.data['verify_key'],
                verify_sign_sha2 = request.data['verify_sign_sha2'],
                currency_type = request.data['currency_type'],
                currency_amount = request.data['currency_amount'],
                currency_rate = request.data['currency_rate'],
                base_fair = request.data['base_fair'],
                value_a = request.data['value_a'],
                value_b = request.data['value_b'],
                value_c = request.data['value_c'],
                value_d = request.data['value_d'],
                subscription_id = request.data['subscription_id'],
                risk_level = request.data['risk_level'],
                risk_title = request.data['risk_title']
            )
        return Response("success", status=status.HTTP_200_OK)


@api_view(['POST'])
def Pro_Payment_fail(request):
    print('::::::::::::::::::',request.data)
    
    return Response("Fail", status=status.HTTP_200_OK)

@api_view(['POST'])
def Pro_Payment_cancle(request):
    print('::::::::::::::::::',request.data)
    return Response("cancle", status=status.HTTP_200_OK)

