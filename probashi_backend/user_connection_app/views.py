from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from auth_user_app.models import User
from user_profile_app.models import User_education



class SearchUserList(views.APIView):
    
    def get(self,request):
        Users = User.objects.all()
        # serializer = StudentSerializer(students,many=True)
        return Response("serializer.data")

    def post(self,request):

        '''
        {
            "EducationDegree" : ["JSC", "SSC", "HSC"],
            "Industry": ["Business", "Software", "Telephone"],
            "Location": ["New York,USA", "London, UK", "Dubai, UAE"]
        }
        '''


        print("request.data",request.data)
        # print('education:::::', request.data['EducationDegree'])

        education_search = User_education.objects.filter(user_edu_degree__in=request.data['EducationDegree'])
        indusrty_search = User.objects.filter(user_industry__in=request.data['Industry'])
        location_search = User.objects.filter(user_geolocation__in=request.data['Location'])
        
        # data = education_search & indusrty_search & location_search
        
        print("edu:::::::",list(education_search))
        print("indusrty:::::::",list(indusrty_search))
        print("location:::::::",list(location_search))
        
        users = User.objects.filter(user_fullname__in=['root','demo2']) 
        # print(users) 


        # serializer = StudentSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()

            # return Response(serializer.data,status=status.HTTP_201_CREATED)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(request.data,status=status.HTTP_201_CREATED)





