from xml.etree.ElementInclude import include
from rest_framework import serializers
from auth_user_app.models import User
from .models import Blog, Blog_comment, Blog_reaction
from drf_extra_fields.fields import Base64ImageField


from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast





class BlogCreateSerializer(serializers.ModelSerializer):
    userblog_addphotopath=Base64ImageField()
    class Meta:
        model = Blog
        fields = '__all__'

class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_comment
        fields = '__all__'

class BlogReactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog_reaction
        fields = '__all__'







class BlogHomePageReactionSerializer(serializers.ModelSerializer):
    # totalliked = serializers.IntegerField(source="is_user_like")

    class Meta:
        model = Blog_reaction
        fields = ['is_user_like', 'is_user_dislike']
    
    
class BlogHomePageCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="userid.user_fullname")
    userphoto = serializers.CharField(source="userid.user_photopath")
    is_consultant = serializers.BooleanField(source="userid.is_consultant")

    class Meta:
        model = Blog_comment
        fields = '__all__'



class BlogPaginateListViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="userid.user_fullname")
    userphoto = serializers.CharField(source="userid.user_photopath")
    is_consultant = serializers.BooleanField(source="userid.is_consultant")
    blog_reaction = BlogHomePageReactionSerializer(many=True, read_only=True)
    blog_comment = BlogHomePageCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = '__all__'