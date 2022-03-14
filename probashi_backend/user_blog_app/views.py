from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .serializers import (BlogCreateSerializer, BlogCommentSerializer,
                            BlogReactionSerializer, BlogSearchSerializer)
from .models import Blog, Blog_reaction, Blog_comment
from rest_framework.pagination import PageNumberPagination


class BlogCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = BlogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BlogListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogCreateSerializer
    queryset = Blog.objects.all()



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
                print('blogid::::::::',request.data['is_user_dislike'])
                Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).delete()
                return Response('delete row',status=status.HTTP_202_ACCEPTED)

        else:
            serializer = BlogReactionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
            return Response('serializer.data',status=status.HTTP_201_CREATED)
        return Response('serializer.errors',status=status.HTTP_400_BAD_REQUEST)


class GetAllusersSetPagination(PageNumberPagination):
    page_size = 20
    # page_size_query_param = 'users'
    max_page_size = 10000

class GetAllUserPaginationView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSearchSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = GetAllusersSetPagination

