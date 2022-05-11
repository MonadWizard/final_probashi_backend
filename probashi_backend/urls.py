import django
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth_user/", include("auth_user_app.urls")),
    path("user_profile/", include("user_profile_app.urls")),
    path("consultancy/", include("consultancy_app.urls")),
    path("user_setting_other_app/", include("user_setting_other_app.urls")),
    path("user_connection/", include("user_connection_app.urls")),
    path("user_blog/", include("user_blog_app.urls")),
    path("user_chat/", include("user_chat_app.urls")),
    path("social-auth/", include("social_auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
