from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import (
    BlogCreateSerializer,
    BlogCommentSerializer,
    BlogReactionSerializer,
    BlogPaginateListViewSerializer,
    SpecificBlogReactionDetailsSerializers,
    SpecificBlogCommentDetailsSerializer,
    AllBlogReactionCountSerializer,
    AllBlogCommentSerializer,
)
from .models import Blog, Blog_reaction, Blog_comment
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from probashi_backend.renderers import UserRenderer
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from .helper import *


class BlogCreateView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]
    serializer_class = BlogCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogCommentView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = [UserRenderer]
    serializer_class = BlogCommentSerializer

    def post(self, request):
        if request.data["userid"] == request.user.userid:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "Userid and Token is invalid", status=status.HTTP_400_BAD_REQUEST
            )


class BlogReactionView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogReactionSerializer

    def post(self, request):
        user = self.request.user
        blog_data = filter_blog_list(request.data["blogid"])
        user_data = filter_user_list(request.data["userid"])
        auth_user_data = filter_auth_user_list(user.userid)
        is_like_data = filter_is_like_data(request.data["is_user_like"])
        is_dislike_data = filter_is_dislike_data(request.data["is_user_dislike"])

        if blog_data & user_data & auth_user_data:
            if blog_data & user_data & is_like_data & is_dislike_data:
                context = {"success": False, "message": "already react happend..."}
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            elif (
                request.data["is_user_like"] == False
                and request.data["is_user_dislike"] == False
            ):
                (blog_data & user_data).update(
                    is_user_like=False, is_user_dislike=False
                )
                update_false = (
                    (blog_data & auth_user_data & is_like_data & is_dislike_data)
                    .values()
                    .order_by("-id")
                )
                context = {"success": True, "data": update_false[0]}
                return Response(context, status=status.HTTP_200_OK)

            elif (
                request.data["is_user_like"] == True
                and request.data["is_user_dislike"] == False
            ):
                (blog_data & auth_user_data).update(
                    is_user_like=True, is_user_dislike=False
                )

                update_true = blog_data.values().order_by("-id")
                context = {"success": True, "data": update_true[0]}
                return Response(context, status=status.HTTP_200_OK)

            elif (
                request.data["is_user_like"] == False
                and request.data["is_user_dislike"] == True
            ):
                (blog_data & auth_user_data).update(
                    is_user_like=False, is_user_dislike=True
                )

                update_false = blog_data.values().order_by("-id")
                context = {"success": True, "data": update_false[0]}
                return Response(context, status=status.HTTP_200_OK)

        elif request.data["userid"] == user.userid:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                serializer.save()
                context = {"success": True, "data": serializer.data}
                return Response(context, status=status.HTTP_200_OK)
        return Response(
            {"success": False, "message": "userid and token is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetAllpostsSetPagination(PageNumberPagination):
    page_size = 15


class BlogPaginateListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BlogPaginateListViewSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsSetPagination
    renderer_classes = [UserRenderer]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_queryset(self):
        data = [self.request.data["tags"]]
        if data == [""]:
            return Blog.objects.all().order_by("-userblog_publishdate")
        else:
            return Blog.objects.filter(userblog_tags__overlap=data).order_by(
                "-userblog_publishdate"
            )


class SpecificBlogReactionDetails(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = SpecificBlogReactionDetailsSerializers
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        blog_id = self.request.query_params.get("id")
        return Blog_reaction.objects.filter(blogid=blog_id)

    def list(self, request):
        userid = request.user.userid
        queryset = self.get_queryset()
        serializer = self.serializer_class(
            queryset, context={"userid": userid}, many=True
        )
        try:
            context = {"data": serializer.data[0]}
        except IndexError:
            context = {"data": "no data"}
        return Response(context, status=status.HTTP_200_OK)


class SpecificBlogCommentDetails(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    renderer_classes = [UserRenderer]
    serializer_class = SpecificBlogCommentDetailsSerializer

    def get_queryset(self):
        user = self.request.user
        blog_id = self.request.query_params.get("id")
        return Blog_comment.objects.filter(Q(userid=user.userid) & Q(blogid=blog_id))

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        try:
            context = {"data": serializer.data}
        except IndexError:
            context = {"data": "no data"}
        return Response(context, status=status.HTTP_200_OK)


class GetAllpostsLikeSetPagination(PageNumberPagination):
    page_size = 15


class BlogPaginateReactionListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AllBlogReactionCountSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsLikeSetPagination
    renderer_classes = [UserRenderer]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_queryset(self):
        return Blog.objects.all().order_by("-userblog_publishdate")


class GetAllpostsCommentSetPagination(PageNumberPagination):
    page_size = 15


class BlogPaginateCommentListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AllBlogCommentSerializer
    queryset = Blog.objects.all()
    pagination_class = GetAllpostsCommentSetPagination
    renderer_classes = [UserRenderer]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_queryset(self):
        return Blog.objects.all().order_by("-userblog_publishdate")
