from django.urls import path
from .views import (BlogCreateView, BlogListView, BlogCommentView,BlogReactionView)



urlpatterns = [
    path('blog-create/', BlogCreateView.as_view(), name="BlogCreateView"),
    path('blog-list/', BlogListView.as_view(), name="BlogListView"),
    path('blog-comment/', BlogCommentView.as_view(), name="BlogCommentView"),
    path('blog-reaction/', BlogReactionView.as_view(), name="BlogReactionView"),
]

