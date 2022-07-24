from import_export import resources
from .models import User, PhoneOTP, mailVerify, user_unmatch


class UserDataPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = ("userid",)


class PhoneOTPPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = PhoneOTP


class mailVerifyPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = mailVerify
        


class user_unmatchPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = user_unmatch
        import_id_fields = ('user_id',)


