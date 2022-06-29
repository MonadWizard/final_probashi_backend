from import_export import resources
from .models import (
    User_socialaccount_and_about,
    User_experience,
    User_education,
    User_idverification,
)

class User_socialaccount_and_aboutPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = User_socialaccount_and_about
        # exclude = ('id',)
        import_id_fields = ("userid",)


class User_experiencePropertyAdminResource(resources.ModelResource):
    class Meta:
        model = User_experience
        import_id_fields = ("userid",)


class User_educationPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = User_education
        # exclude = ('id',)
        import_id_fields = ("userid",)


class User_idverificationPropertyAdminResource(resources.ModelResource):
    class Meta:
        model = User_idverification
        # exclude = ('id',)
        import_id_fields = ("userid",)
