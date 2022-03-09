from django.db import models
from auth_user_app.models import User

# Create your models here.


class StaticSettingData(models.Model):
    class Meta:
        db_table = 'static_setting_data'
        verbose_name = 'static_setting_data'
        verbose_name_plural = 'static_setting_data'

    user_industry_data = models.CharField(max_length=255, unique=True, blank=True, null=True)
    user_areaof_experience_data = models.CharField(max_length=255, unique=True, blank=True, null=True)
    user_interested_area_data = models.CharField(max_length=255, unique=True, blank=True, null=True)
    user_goal_data = models.CharField(max_length=255, unique=True, blank=True, null=True)
    consultancyservice_category_data = models.CharField(max_length=255, unique=True, blank=True, null=True)

    def __str__(self):
        if self.user_industry_data:
            return self.user_industry_data
        elif self.user_areaof_experience_data:
            return self.user_areaof_experience_data
        elif self.user_interested_area_data:
            return self.user_interested_area_data
        elif self.user_goal_data:
            return self.user_goal_data
        elif self.consultancyservice_category_data:
            return self.consultancyservice_category_data
        else:
            return 'No Data'



class Promo_code_data(models.Model):
    promo_code = models.CharField(primary_key=True, max_length=200, unique=True, db_index=True)
    promo_code_point = models.IntegerField(default=0)
    promo_code_status = models.BooleanField(default=False)
    promo_code_start_date = models.DateField(blank=True, null=True)
    promo_code_end_date = models.DateField(blank=True, null=True)


class User_settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    user_mail_notification_enable = models.BooleanField(default=True)
    user_monthly_newsleter_enable = models.BooleanField(default=True)
    user_reward_point = models.IntegerField(default=0)
    # user_promo_code_pk = 

class Facing_trouble(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    user_problem_message = models.TextField(blank=True, null=True)
    user_problem_photo_path = models.CharField(max_length=200, blank=True, null=True)
