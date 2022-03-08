from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from auth_user_app.models import User
from user_profile_app.models import User_education
from .serializers import SerachUserSerializer
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination



class SearchUserList(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request):
        Users = User.objects.all()
        # serializer = StudentSerializer(students,many=True)
        return Response("serializer.data")

    def post(self,request):

        '''
        {
            "EducationDegree" : ["JSC", "SSC", "HSC", "BllaBlla", "BllaBlla2"],
            "Industry": ["Business", "Software", "Telephone","New Indrustry", "New Indrustry 2"],
            "Location": ["New York,USA", "London,UK", "Dubai,UAE"]
        }
        '''

        input_data = request.data['input_data']
        input_data_search = (Q(user_fullname__icontains = input_data) or \
                            Q(user_email__icontains = input_data) or \
                            Q(user_username__icontains = input_data))

        input_serached_data = User.objects.filter(input_data_search).values_list('userid', flat=True)

        # print("input_serached_data::::::::::",input_serached_data)                    
        
        
        
        # education_search = list(User_education.objects.filter(user_edu_degree__in=request.data['EducationDegree']).values_list('userid', flat=True))
        # indusrty_search = list(User.objects.filter(user_industry__in=request.data['Industry']).values_list('userid', flat=True))
        # location_search = list(User.objects.filter(user_geolocation__in=request.data['Location']).values_list('userid', flat=True))

        input_data_search = (Q(user_fullname__icontains = request.data['input_data']) or \
                            Q(user_email__icontains = request.data['input_data']) or \
                            Q(user_username__icontains = request.data['input_data']))

        choise_data_Search = (Q(user_edu_degree__in=request.data['EducationDegree']) and \
                            Q(user_industry__in=request.data['Industry']) and \
                            Q(user_geolocation__in=request.data['Location']))    

        input_serached_data = User.objects.filter(input_data_search)
        choise_search_data = User.objects.filter(choise_data_Search)
        print("choise_search_data::::::::::",choise_search_data)
        print("input_serached_data::::::::::",input_serached_data)
        # searched =list(set(education_search) & set(indusrty_search) & set(location_search) | set(input_serached_data))    
        searched = list(set(choise_search_data) | set(input_serached_data))
        print("searched::::::::::",searched)
        
        searched_user = User.objects.filter(userid__in=searched)

        serializer = SerachUserSerializer(searched_user,many=True)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)


class GetAllusersSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'users'
    max_page_size = 10000

class GetAllUserPaginationView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SerachUserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = GetAllusersSetPagination





