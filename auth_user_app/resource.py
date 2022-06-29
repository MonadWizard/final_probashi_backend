from import_export import resources
from .models import User, PhoneOTP, mailVerify, user_unmatch


class UserDataPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = User
        # exclude = ('id',)
        import_id_fields = ("userid",)


class PhoneOTPPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = PhoneOTP
        # import_id_fields = ('id',)


class mailVerifyPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = mailVerify
        # exclude = ('id',)
        # import_id_fields = ("userid",)


class user_unmatchPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = user_unmatch
        import_id_fields = ('user_id',)


