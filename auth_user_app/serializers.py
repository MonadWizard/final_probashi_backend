from rest_framework import serializers
from .models import User, PhoneOTP, mailVerify
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_extra_fields.fields import Base64ImageField

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .customAuth import CustomerBackendForPhoneNumber

import time


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    userid = serializers.CharField(max_length=68, min_length=6, write_only=True)

    
    class Meta:
        model = User
        fields = ["userid", "user_email", "user_fullname", "password"]

    

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UpdateRegisterSerializer(serializers.ModelSerializer):
    user_photopath = Base64ImageField()  # From DRF Extra Fields

    class Meta:
        model = User
        fields = [
            "user_fullname",
            "user_username",
            "user_gender",
            "user_dob",
            "user_photopath",
            "user_device_typeserial",
            "user_geolocation",
            "user_residential_district",
            "user_nonresidential_country",
            "user_nonresidential_city",
            "user_durationyear_abroad",
        ]

    def create(self, validated_data):
        user_photopath = validated_data.pop("user_photopath")
        return User.objects.create(user_photopath=user_photopath)


class LoginSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(user_email=obj["user_email"])

        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    class Meta:
        model = User
        fields = ["user_email", "password", "tokens"]

    def validate(self, attrs):
        user_email = attrs.get("user_email", "")
        password = attrs.get("password", "")
        try:
            user = User.objects.get(user_email=user_email)
            filtered_user_by_email = user.user_email
            print("filtered_user_by_email", user.auth_provider)
            user = None
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist")

        
        try:

            user = auth.authenticate(user_email=user_email, password=password)

        except:
            if filtered_user_by_email != user_email:
                raise serializers.ValidationError(
                    detail="Please continue your login using " + user.auth_provider
                )

            if not user:
                raise serializers.ValidationError("Invalid credentials, try again")

            if not user.is_active:
                raise serializers.ValidationError("Account disabled, contact admin")
            if not user.is_verified:
                raise serializers.ValidationError("Email is not verified")

            if user is None:
                raise serializers.ValidationError("Invalid credentials")
            else:
                return attrs

        

        return {"user_email": user.user_email, "tokens": user.tokens}



class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    user_email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ["user_email"]


class SetNewPasswordSerializer(serializers.Serializer):
    model = User

    userid = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):

        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")


class UserEmailandPasswordChangeSerializer(serializers.Serializer):
    model = User

    user_email = serializers.EmailField(required=False)
    new_password = serializers.CharField(required=False)


class InAppChangePasswordSerializer(serializers.Serializer):
    model = User

    user_email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True)


class InAppChangeOnlyPasswordSerializer(serializers.Serializer):
    model = User
    new_password = serializers.CharField(required=True)


class InAppChangeOnlyEmailSerializer(serializers.Serializer):
    model = User
    user_email = serializers.EmailField(required=True)


class RequestPasswordResetEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = "__all__"




class userOTP(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTP
        fields = "__all__"


class PhoneOtpRegisterSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["userid", "user_callphone", "user_fullname"]

    def create(self, validated_data):
        return User.objects.create_user_phone(**validated_data)


class PhoneLoginSerializer(serializers.ModelSerializer):
    user_callphone = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(user_callphone=obj["user_callphone"])
        if user.is_active:
            return {
                "refresh": user.tokens()["refresh"],
                "access": user.tokens()["access"],
            }

    class Meta:
        model = User
        fields = ["user_callphone", "tokens"]

    def validate(self, attrs):
        user_callphone = attrs.get("user_callphone", "")
        filtered_user_by_user_callphone = User.objects.filter(
            user_callphone=user_callphone
        )

        user = None
        try:
            user = CustomerBackendForPhoneNumber.authenticate(
                user_callphone=user_callphone
            )

        except:
            if not user:
                raise serializers.ValidationError("Invalid credentials, try again")
            if not user.is_active:
                raise serializers.ValidationError("Account disabled, contact admin")
            if not user.is_verified:
                raise serializers.ValidationError("Phone is not verified")
            if user is None:
                raise serializers.ValidationError("Invalid credentials")
            else:
                return attrs

        return {"user_callphone": user.user_callphone, "tokens": user.tokens}


class takeVarifiedEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = mailVerify
        fields = "__all__"
