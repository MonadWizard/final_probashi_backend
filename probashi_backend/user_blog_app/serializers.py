from xml.etree.ElementInclude import include
from rest_framework import serializers
from auth_user_app.models import User
from .models import Blog, Blog_comment, Blog_reaction
from drf_extra_fields.fields import Base64ImageField





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




class BlogSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog_reaction
        fields = '__all__'




