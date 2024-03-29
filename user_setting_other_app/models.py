from django.db import models
from auth_user_app.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class StaticSettingData(models.Model):
    class Meta:
        db_table = "static_setting_data"
        verbose_name = "static_setting_data"
        verbose_name_plural = "static_setting_data"

    user_industry_data = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    user_current_designation = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    
    user_areaof_experience_data = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    user_interested_area_data = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    user_goal_data = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    consultancyservice_category_data = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    blog_tags_data = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    user_education_data = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )

    faq_title = models.CharField(max_length=255, unique=True, blank=True, null=True)
    faq_description = models.TextField(blank=True, null=True)

    privacypolicy_title = models.CharField(
        max_length=255, unique=True, blank=True, null=True
    )
    privacypolicy_descriptions = models.TextField(blank=True, null=True)

    # Education Service
    educationService_degree = models.CharField(max_length=200, blank=True, null=True)
    # Overseas Recruitment Service
    overseasrecruitmentservice_job_type = models.CharField(
        max_length=200, blank=True, null=True
    )
    # Medical Consultancy Service
    medicalconsultancyservice_treatment_area = models.CharField(
        max_length=200, blank=True, null=True
    )
    # Legal&Civil Service
    legalcivilservice_required = models.CharField(max_length=200, blank=True, null=True)
    legalcivilservice_issue = models.CharField(max_length=200, blank=True, null=True)
    # Property Management Service
    propertymanagementservice_propertylocation = models.CharField(
        max_length=200, blank=True, null=True
    )
    propertymanagementservice_type = models.CharField(
        max_length=200, blank=True, null=True
    )
    propertymanagementservice_need = models.CharField(
        max_length=200, blank=True, null=True
    )
    # Tourism Service
    tourismservices = models.CharField(max_length=200, blank=True, null=True)
    # Training Service
    trainingservice_topic = models.CharField(max_length=200, blank=True, null=True)
    trainingservice_duration = models.CharField(max_length=200, blank=True, null=True)
    # Digital Service
    digitalservice_type = models.CharField(max_length=200, blank=True, null=True)
    # Trade Facilitation Service
    tradefacilitationservice_type = models.CharField(
        max_length=200, blank=True, null=True
    )
    tradefacilitationservice_Purpose = models.CharField(
        max_length=200, blank=True, null=True
    )
    country_name = models.CharField(max_length=200, blank=True, null=True)
    state_name = ArrayField(models.CharField(max_length=200), blank=True, null=True)


class PromoCodeData(models.Model):
    promo_code = models.CharField(
        primary_key=True, max_length=200, unique=True, db_index=True
    )
    promo_code_point = models.IntegerField(default=0)
    promo_code_amount = models.IntegerField(default=0)
    is_promo_code_active = models.BooleanField(default=False)

    # class Meta:
    #     db_table = 'PromoCodeData'
    #     # verbose_name = 'promo_code_data'
    # verbose_name_plural = 'promo_code_data'

    def __str__(self):
        return str(self.promo_code) if self.promo_code else "No Data"


class User_settings(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE)
    user_mail_notification_enable = models.BooleanField(default=True)
    user_monthly_newsleter_enable = models.BooleanField(default=True)
    user_reward_point = models.IntegerField(default=0)

    class Meta:
        # db_table = 'User_settings'
        # verbose_name = 'user_settings'
        verbose_name_plural = 'user_settings'

class Facing_trouble(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_problem_message = models.TextField(blank=True, null=True)
    user_problem_photo_path = models.ImageField(
        upload_to="probashi_app/facing_trouble", blank=True, null=True
    )


class Notification(models.Model):
    userid = models.ForeignKey(
        User, related_name="notification_user", on_delete=models.CASCADE
    )
    receiverid = models.ForeignKey(
        User, related_name="notification_receiver", on_delete=models.CASCADE
    )
    notification_title = models.CharField(max_length=255, blank=True, null=True)
    notification_description = models.TextField(blank=True, null=True)
    is_notification_seen = models.BooleanField(default=False)
    notification_date = models.DateTimeField(auto_now_add=True)
    is_notification_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.notification_title) if self.notification_title else "No Data"


class Probashi_administrative_payment(models.Model):
    pro_user_payment = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.pro_user_payment) if self.pro_user_payment else "No Data"




