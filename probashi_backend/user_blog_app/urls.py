from django.urls import path
from .views import (BlogCreateView, BlogPaginateListView, BlogCommentView,BlogReactionView)



urlpatterns = [
    path('blog-create/', BlogCreateView.as_view(), name="BlogCreateView"),
    path('blog-list/', BlogPaginateListView.as_view(), name="BlogPaginateListView"),
    path('blog-comment/', BlogCommentView.as_view(), name="BlogCommentView"),
    path('blog-reaction/', BlogReactionView.as_view(), name="BlogReactionView"),
]

