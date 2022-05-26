from django.apps import AppConfig


class AuthUserAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_user_app"

    def ready(self):
        from . signals import  post_delete_action
        

        