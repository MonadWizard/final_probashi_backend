from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from auth_user_app.models import User
from user_profile_app.models import User_education
from .serializers import SerachUserSerializer



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

        education_search = list(User_education.objects.filter(user_edu_degree__in=request.data['EducationDegree']).values_list('userid', flat=True))
        indusrty_search = list(User.objects.filter(user_industry__in=request.data['Industry']).values_list('userid', flat=True))
        location_search = list(User.objects.filter(user_geolocation__in=request.data['Location']).values_list('userid', flat=True))

        searched =list(set(education_search) & set(indusrty_search) & set(location_search))    
        searched_user = User.objects.filter(userid__in=searched)

        serializer = SerachUserSerializer(searched_user,many=True)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)





