from multiprocessing import context
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .models import StaticSettingData
from .serializers import (UserIndustryDataSerializer,
                    UserAreaOfExperienceDataSerializer,
                    UserInterestedAreaDataSerializer,
                    UserGoalDataSerializer,
                    ConsultancyServiceCategoryDataSerializer,
                    CreateOtherRowsInStatictableSerializer,
                    BlogTagDataSerializers)





class CreateOtherRowsInStaticTableView(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated,]

    # permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.all()
    serializer_class= CreateOtherRowsInStatictableSerializer



class UserIndustryDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_industry_data__isnull=False)
    serializer_class= UserIndustryDataSerializer

    def post(self, request):
        serializer = UserIndustryDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errorcontext = {'user_industry_data': serializer.errors['user_industry_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)



    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserIndustryDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)



class UserAreaOfExperienceDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]    
    queryset = StaticSettingData.objects.filter(user_areaof_experience_data__isnull=False)
    serializer_class= UserAreaOfExperienceDataSerializer
    
    def post(self, request):
        serializer = UserAreaOfExperienceDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errorcontext = {'user_areaof_experience_data': serializer.errors['user_areaof_experience_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserAreaOfExperienceDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)



class UserInterestedAreaDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_interested_area_data__isnull=False)
    serializer_class= UserInterestedAreaDataSerializer

    def post(self, request):
        serializer = UserInterestedAreaDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errorcontext = {'user_interested_area_data': serializer.errors['user_interested_area_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserInterestedAreaDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)




class UserGoalDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(user_goal_data__isnull=False)
    serializer_class= UserGoalDataSerializer

    def post(self, request):
        serializer = UserGoalDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errorcontext = {'user_goal_data': serializer.errors['user_goal_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserGoalDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)




class ConsultancyServiceCategoryDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(consultancyservice_category_data__isnull=False)
    serializer_class= ConsultancyServiceCategoryDataSerializer


    def post(self, request):
        serializer = ConsultancyServiceCategoryDataSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errorcontext = {'consultancyservice_category_data': serializer.errors['consultancyservice_category_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = ConsultancyServiceCategoryDataSerializer(queryset, many=True)
        context = {"data":serializer.data}
        return Response(context, status=status.HTTP_200_OK)





class BlogTagDataView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    queryset = StaticSettingData.objects.filter(blog_tags_data__isnull=False)
    serializer_class= BlogTagDataSerializers

    def post(self, request):
        serializer = BlogTagDataSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errorcontext = {'blog_tags_data': serializer.errors['blog_tags_data'][0]}
        return Response(errorcontext, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):
        queryset = self.get_queryset()
        serializer = BlogTagDataSerializers(queryset, many=True)
        # context = {"data":serializer.data}
        tags = []
        for data in serializer.data:
            data['blog_tags_data'] = data['blog_tags_data'].split(',')
            # print(data['blog_tags_data'])
            tags += data['blog_tags_data'] 
        # print(tags)
        context = {"data":tags}
        return Response(context, status=status.HTTP_200_OK)





