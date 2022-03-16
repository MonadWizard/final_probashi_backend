from multiprocessing import context
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .serializers import (BlogCreateSerializer, BlogCommentSerializer,
                            BlogReactionSerializer,
                            BlogPaginateListViewSerializer, BlogHomePageReactionSerializer)
from .models import Blog, Blog_reaction, Blog_comment
from rest_framework.pagination import PageNumberPagination

from django.db.models import Case, IntegerField, Sum, When



class BlogCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = BlogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BlogCommentView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = BlogCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BlogReactionView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):

        if Blog_reaction.objects.filter(blogid__exact=request.data['blogid']):
            if request.data['is_user_like'] == False and request.data['is_user_dislike'] == False:
                # print('blogid::::::::',request.data['is_user_dislike'])
                Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).delete()

                return Response('delete row',status=status.HTTP_202_ACCEPTED)

            if request.data['is_user_like'] == True and request.data['is_user_dislike'] == False:
                return Response('already Liked',status=status.HTTP_400_BAD_REQUEST)
            if request.data['is_user_like'] == False and request.data['is_user_dislike'] == True:
                return Response('already disliked',status=status.HTTP_400_BAD_REQUEST)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        else:
            serializer = BlogReactionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class GetAllpostsSetPagination(PageNumberPagination):
    page_size = 10

class BlogPaginateListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogPaginateListViewSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsSetPagination

    def get_queryset(self):
        return Blog.objects.all().order_by('-userblog_publishdate')

















