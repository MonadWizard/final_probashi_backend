# all search queries

from .models import Blog, Blog_comment, Blog_reaction
from django.db.models import Q


def filter_blog_list(data):
    # print("data", data)
    try:
        return Blog_reaction.objects.filter(blogid__exact=data)
    except Exception as e:
        print("Exception:::", e)
        return None


def filter_user_list(data):
    try:
        return Blog_reaction.objects.filter(userid__exact=data)
    except Exception as e:
        print("Exception:::", e)
        return None


def filter_auth_user_list(data):
    try:
        return Blog_reaction.objects.filter(userid__exact=data)
    except Exception as e:
        print("Exception:::", e)
        return None


def filter_is_like_data(data):
    try:
        return Blog_reaction.objects.filter(is_user_like=data)
    except Exception as e:
        print("Exception:::", e)
        return None


def filter_is_dislike_data(data):
    try:
        return Blog_reaction.objects.filter(is_user_dislike=data)
    except Exception as e:
        print("Exception:::", e)
        return None
