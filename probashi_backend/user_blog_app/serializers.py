from xml.etree.ElementInclude import include
from rest_framework import serializers
from auth_user_app.models import User
from .models import Blog, Blog_comment, Blog_reaction
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Q

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

    class Meta:
        model = Blog_reaction
        fields = '__all__'
    
    
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
    # blog_reaction = BlogHomePageReactionSerializer(many=True, read_only=True)
    blog_comment = BlogHomePageCommentSerializer(many=True, read_only=True)
    totalliked = serializers.SerializerMethodField('get_total_like')
    totaldisliked = serializers.SerializerMethodField('get_total_dislike')



    def get_total_like(self, obj):
        # print(self.context)
        return Blog_reaction.objects.filter(Q(blogid=obj.id) & Q(is_user_like=True)).count()
    
    def get_total_dislike(self, obj):
        return Blog_reaction.objects.filter(Q(blogid=obj.id) & Q(is_user_dislike=True)).count()

    class Meta:
        model = Blog
        fields = '__all__'


