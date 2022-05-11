from django.urls import path
from .views import (
    BlogCreateView,
    BlogPaginateListView,
    BlogCommentView,
    BlogReactionView,
    SpecificBlogReactionDetails,
    SpecificBlogCommentDetails,
    BlogPaginateReactionListView,
    BlogPaginateCommentListView,
)


urlpatterns = [
    path("blog-create/", BlogCreateView.as_view(), name="BlogCreateView"),
    path("blog-list/", BlogPaginateListView.as_view(), name="BlogPaginateListView"),
    path("blog-comment/", BlogCommentView.as_view(), name="BlogCommentView"),
    path("blog-reaction/", BlogReactionView.as_view(), name="BlogReactionView"),
    path(
        "specific-blog-reaction/",
        SpecificBlogReactionDetails.as_view(),
        name="SpecificBlogReactionDetails",
    ),
    path(
        "specific-blog-comments/",
        SpecificBlogCommentDetails.as_view(),
        name="SpecificBlogCommentDetails",
    ),
    path(
        "blog-reaction-list/",
        BlogPaginateReactionListView.as_view(),
        name="BlogPaginateReactionListView",
    ),
    path(
        "blog-comment-list/",
        BlogPaginateCommentListView.as_view(),
        name="BlogPaginateCommentListView",
    ),
    # path('blog-search/', BlogSearch.as_view(), name="BlogSearch"),
]
