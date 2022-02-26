
from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    userid = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'email': 'The email should only contain alphanumeric characters'}
    
    class Meta:
        model = User
        fields = ['userid','user_email', 'user_fullname', 'password']

    def validate(self, attrs):
        userid = attrs.get('userid', '')
        user_email = attrs.get('user_email', '')
        user_fullname = attrs.get('user_fullname', '')
        print('attrs', attrs)

        # # validet fullname is allphanumeric
        # if not fullname.isalnum():
        #     raise serializers.ValidationError(
        #         self.default_error_messages)
        
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    # user_fullname = serializers.CharField(
    #     max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(user_email=obj['user_email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['user_email', 'password', 'tokens']

    def validate(self, attrs):
        user_email = attrs.get('user_email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(user_email=user_email)
        user = auth.authenticate(user_email=user_email, password=password)

        print("filtered_user_by_email::::::",filtered_user_by_email[0])
        print("user_email::::::",type(user_email))
        print("filtered_user_by_email[0].auth_provider::::::",str(filtered_user_by_email[0]) != user_email)

        if filtered_user_by_email.exists() and str(filtered_user_by_email[0]) != user_email:
            raise AuthenticationFailed(detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'user_email': user.user_email,
            'tokens': user.tokens
        }

        return super().validate(attrs)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    user_email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ['user_email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(userid=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):

        self.token = attrs['refresh']
        print("refresh::::::",self.token)

        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            # self.fail(self.default_error_message)
            raise AuthenticationFailed("except TokenError")


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

