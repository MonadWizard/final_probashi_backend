from multiprocessing import context
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions
from django.http import Http404
from .serializers import (BlogCreateSerializer, BlogCommentSerializer,
                            BlogReactionSerializer,
                            BlogPaginateListViewSerializer, 
                            BlogHomePageReactionSerializer,
                            SpecificBlogReactionDetailsSerializers,
                            SpecificBlogCommentDetailsSerializer,
                            AllBlogReactionCountSerializer,
                            AllBlogCommentSerializer)
from .models import Blog, Blog_reaction, Blog_comment
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from auth_user_app.models import User
from probashi_backend.renderers import UserRenderer
import json
from django.db import connection
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination





class BlogCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def post(self,request):
        serializer = BlogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BlogCommentView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]

    def post(self,request):
        # print('user:::::::',request.user.userid)
        if request.data['userid'] == request.user.userid:
            serializer = BlogCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Userid and Token is invalid',status=status.HTTP_400_BAD_REQUEST)

class BlogReactionView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # renderer_classes = [UserRenderer]

    def post(self,request):

        user = self.request.user

        if Blog_reaction.objects.filter(Q(blogid__exact=request.data['blogid']) & Q(userid__exact=user.userid) & Q(userid__exact=request.data['userid'])).exists():
            if request.data['is_user_like'] == False and request.data['is_user_dislike'] == False:
                # Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).delete()
                Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).update(is_user_like=False,is_user_dislike=False)
                update_false = Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).values()
                # Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).delete()
                print('::::::::::', list(update_false)[0])
                context = {'success': True, 'data': list(update_false)[-1]}
                # context.update(list(update_false))    
                return Response(context,status=status.HTTP_202_ACCEPTED)
                # return Response('user can like or dislike',status=status.HTTP_202_ACCEPTED)

            elif Blog_reaction.objects.filter(Q(is_user_like=request.data['is_user_like']) & 
                                                Q(is_user_dislike=request.data['is_user_dislike'])).exists():
                context = {'success': False, 'message': 'already react happend'}
                return Response(context,status=status.HTTP_400_BAD_REQUEST)

            
            else:
                serializer = BlogReactionSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    context = {'success': True, 'data': serializer.data}
                    # context.update(serializer.data)
                    return Response(context ,status=status.HTTP_200_OK)

        
        elif request.data['userid'] == user.userid : 
            serializer = BlogReactionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                context = {'success': True, 'data': serializer.data}
                # context.update(serializer.data)
                return Response(context ,status=status.HTTP_200_OK)
        return Response({'success': False, 'message':'userid and token is invalid'},status=status.HTTP_400_BAD_REQUEST)


class GetAllpostsSetPagination(PageNumberPagination):
    page_size = 3

class BlogPaginateListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogPaginateListViewSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsSetPagination
    renderer_classes = [UserRenderer]

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return Blog.objects.all().order_by('-userblog_publishdate')



# specific blog share link.............



class SpecificBlogReactionDetails(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = SpecificBlogReactionDetailsSerializers
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
            user = self.request.user
            blog_id = self.request.query_params.get('id')
            # print("blog_id:::", blog_id)
            return Blog_reaction.objects.filter(blogid=blog_id)

    def list(self, request):
        userid = request.user.userid
        # print("user::::", userid)
        queryset = self.get_queryset()
        # print("queryset:::", queryset)
        serializer = SpecificBlogReactionDetailsSerializers(queryset,context={'userid':userid}, many=True)
        try:
            context = {"data": serializer.data[0]}
        except IndexError:
            context = {"data": "no data"}
        return Response(context, status=status.HTTP_200_OK)



class SpecificBlogCommentDetails(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = SpecificBlogReactionDetailsSerializers
    renderer_classes = [UserRenderer]
    
    def get_queryset(self):
            user = self.request.user
            blog_id = self.request.query_params.get('id')
            return Blog_comment.objects.filter(Q(userid=user.userid) & Q(blogid=blog_id))

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SpecificBlogCommentDetailsSerializer(queryset, many=True)
        try:
            context = {"data": serializer.data}
        except IndexError:
            context = {"data": "no data"}
        return Response(context, status=status.HTTP_200_OK)



class GetAllpostsLikeSetPagination(PageNumberPagination):
    page_size = 3

class BlogPaginateReactionListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AllBlogReactionCountSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsLikeSetPagination
    renderer_classes = [UserRenderer]

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return Blog.objects.all().order_by('-userblog_publishdate')




class GetAllpostsCommentSetPagination(PageNumberPagination):
    page_size = 3

class BlogPaginateCommentListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AllBlogCommentSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsCommentSetPagination
    renderer_classes = [UserRenderer]

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return Blog.objects.all().order_by('-userblog_publishdate')




class GetBlogPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


# user blog Search..............
# select * from public.user_blog_app_blog
# where userblog_tags @> '{"tag1"}';

class BlogSearch(views.APIView):
    # permission_classes = [permissions.IsAuthenticated,]
    # renderer_classes = [UserRenderer]

    # search Blog Tags
        # give list of tags
        # I use cursor.fatchall()
        # give response as pagination  view 
    def post(self, request):
        tags = request.data['tags']
        print("request data::::::",type(tags))

        query = "select * from public.user_blog_app_blog where userblog_tags @> '{" 
        query += str(tags[::])[1:-1].replace("'", '"')
        query += "}'; "
        # print("query:::", query)

        with connection.cursor() as cursor:
            cursor.execute(query)
            q_data_fatch_all = cursor.fetchall()

        result = []
        columnNames = [column[0] for column in cursor.description]

        for record in q_data_fatch_all:
            result.append( dict( zip( columnNames , record ) ) )

        context = {'success': True, 'data': result}    
        
        paginator = GetBlogPagination()
        page = paginator.paginate_queryset(result, request)
        if page is not None:
            # print("is not none::::::::::::::::::::::", page)
            return paginator.get_paginated_response(page)
        
        # print("::::::::::::::::::::::", page)

        return Response(page, status=status.HTTP_200_OK)
        
        
        
        # return Response(context, status=status.HTTP_200_OK)



################# need to be pagination..........



