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





class BlogCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = BlogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BlogCommentView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):
        serializer = BlogCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BlogReactionView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self,request):

        user = self.request.user
        # user_id = User.objects.filter(user_email=user).values('userid')
        # user_id = user_id[0].get('userid')

        if Blog_reaction.objects.filter(Q(blogid__exact=request.data['blogid']) & Q(userid__exact=user.userid)).exists():
            if request.data['is_user_like'] == False and request.data['is_user_dislike'] == False:
                # Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).delete()
                Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).update(is_user_like=False,is_user_dislike=False)
                update_false = Blog_reaction.objects.filter(blogid__exact=request.data['blogid']).values()

                return Response(update_false,status=status.HTTP_202_ACCEPTED)

            elif Blog_reaction.objects.filter(Q(is_user_like=request.data['is_user_like']) & 
                                                Q(is_user_dislike=request.data['is_user_dislike'])).exists():
                return Response('already react happend',status=status.HTTP_400_BAD_REQUEST)

            
            else:
                serializer = BlogReactionSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data ,status=status.HTTP_200_OK)

        
        elif request.data['userid'] == user.userid : 
            serializer = BlogReactionSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data ,status=status.HTTP_200_OK)
        return Response('bad request',status=status.HTTP_400_BAD_REQUEST)


class GetAllpostsSetPagination(PageNumberPagination):
    page_size = 3

class BlogPaginateListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogPaginateListViewSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsSetPagination

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return Blog.objects.all().order_by('-userblog_publishdate')




class SpecificBlogReactionDetails(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = SpecificBlogReactionDetailsSerializers
    
    def get_queryset(self):
            user = self.request.user
            blog_id = self.request.query_params.get('id')
            return Blog_reaction.objects.filter(Q(userid=user.userid) & Q(blogid=blog_id))

    def list(self, request):
        queryset = self.get_queryset()
        serializer = SpecificBlogReactionDetailsSerializers(queryset, many=True)
        try:
            context = {"data": serializer.data[0]}
        except IndexError:
            context = {"data": "no data"}
        return Response(context, status=status.HTTP_200_OK)



class SpecificBlogCommentDetails(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    # serializer_class = SpecificBlogReactionDetailsSerializers
    
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

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_queryset(self):
        return Blog.objects.all().order_by('-userblog_publishdate')

