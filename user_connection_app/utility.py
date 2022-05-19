from auth_user_app.models import User
from .models import FriendsSuggation, UserFavouriteList
from django.db.models import Q
from asgiref.sync import sync_to_async


def get_or_create_friend_suggestion(user):
    try:
        suggestion = FriendsSuggation.objects.get(user=user.userid)
    except:
        suggestion = FriendsSuggation.objects.create(user=user)

    suggestion.location = [] if suggestion.location is None else suggestion.location
    suggestion.goals = [] if suggestion.goals is None else suggestion.goals
    suggestion.interest = [] if suggestion.interest is None else suggestion.interest
    suggestion.durationyear_abroad = [] if suggestion.durationyear_abroad is None else suggestion.durationyear_abroad
    suggestion.current_location_durationyear = [] if suggestion.current_location_durationyear is None else suggestion.current_location_durationyear
    suggestion.industry = [] if suggestion.industry is None else suggestion.industry
    suggestion.areaof_experience = [] if suggestion.areaof_experience is None else suggestion.areaof_experience
    suggestion.industry_experienceyear = [] if suggestion.industry_experienceyear is None else suggestion.industry_experienceyear
    suggestion.serviceholder = [] if suggestion.serviceholder is None else suggestion.serviceholder
    suggestion.selfemployed = [] if suggestion.selfemployed is None else suggestion.selfemployed
    suggestion.currentdesignation = [] if suggestion.currentdesignation is None else suggestion.currentdesignation
    suggestion.company_name = [] if suggestion.company_name is None else suggestion.company_name
    suggestion.office_address = [] if suggestion.office_address is None else suggestion.office_address
    
    return suggestion

def append_item_in_list(user_obj,rest_obj, user_friend_suggestion_obj, rest_friend_suggestion_obj, friend_suggestion_attribute):

    rest_values = getattr(rest_friend_suggestion_obj, friend_suggestion_attribute)
    user_values = getattr(user_friend_suggestion_obj, friend_suggestion_attribute)

    if user_obj.userid not in rest_values:
        rest_values.append(user_obj.userid)

    if (rest_obj.userid not in user_values):
        user_values.append(rest_obj.userid)

def update_friendsuggestion(user_obj,rest_obj, user_friend_suggestion_obj, rest_friend_suggestion_obj, user_attribute, friend_suggestion_attribute, type):
    if type == 'string':
        if (
            getattr(rest_obj, user_attribute) is not None
            and getattr(rest_obj, user_attribute) != ""
            and getattr(rest_obj, user_attribute) == getattr(user_obj, user_attribute)
            ):
            append_item_in_list(user_obj,rest_obj, user_friend_suggestion_obj, rest_friend_suggestion_obj, friend_suggestion_attribute)
    
    elif type == 'list':
        if (getattr(rest_obj, user_attribute) is not None
            and (set(getattr(rest_obj, user_attribute)) & set(getattr(user_obj, user_attribute)))):

            append_item_in_list(user_obj,rest_obj, user_friend_suggestion_obj, rest_friend_suggestion_obj, friend_suggestion_attribute)
    
    elif type == 'bool':
        if getattr(rest_obj, user_attribute) == getattr(user_obj, user_attribute):
            append_item_in_list(user_obj,rest_obj, user_friend_suggestion_obj, rest_friend_suggestion_obj, friend_suggestion_attribute)
    else:
        pass
            

@sync_to_async
def match_friends(user_id):
    user = User.objects.get(userid=user_id)
    user_goal = user.user_goal if user.user_goal else []
    user_interested_area = (
        user.user_interested_area if user.user_interested_area else []
    )
    rest_users = User.objects.filter(
        (
            (
                Q(user_residential_district__iexact=user.user_residential_district)
                & Q(user_residential_district__isnull=False)
            )
            | (
                Q(user_nonresidential_city__iexact=user.user_nonresidential_city)
                & Q(user_nonresidential_city__isnull=False)
            )
            | Q(user_goal__contains=user_goal)
            | Q(user_interested_area__contains=user_interested_area)
        )
        & ~Q(userid=user_id)
        & Q(is_active=True)
        & ~Q(is_staff=True)
        & ~Q(
            userid__in=UserFavouriteList.objects.filter(userid=user.userid).values(
                "userid"
            )
        )
        | (
            Q(user_durationyear_abroad=user.user_durationyear_abroad)
            & Q(user_durationyear_abroad__isnull=False)
        )
        | (
            Q(
                user_current_location_durationyear=user.user_current_location_durationyear
            )
            & Q(user_current_location_durationyear__isnull=False)
        )
        | (Q(user_industry=user.user_industry) & Q(user_industry__isnull=False))
        | (
            Q(user_areaof_experience=user.user_areaof_experience)
            & Q(user_areaof_experience__isnull=False)
        )
        | (
            Q(user_industry_experienceyear=user.user_industry_experienceyear)
            & Q(user_industry_experienceyear__isnull=False)
        )
        | Q(is_user_serviceholder=user.is_user_serviceholder)
        | Q(is_user_selfemployed=user.is_user_selfemployed)
        | (
            Q(user_currentdesignation__iexact=user.user_currentdesignation)
            & Q(user_currentdesignation__isnull=False)
        )
        | (
            Q(user_company_name__iexact=user.user_company_name)
            & Q(user_company_name__isnull=False)
        )
        | (
            Q(user_office_address__iexact=user.user_office_address)
            & Q(user_office_address__isnull=False)
        )
    )

    user_friendsuggestion = get_or_create_friend_suggestion(user)

    for rest_user in rest_users:
        friendsuggestion = get_or_create_friend_suggestion(rest_user)
        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_residential_district", "location", 'string')
        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_nonresidential_city", "location", 'string')
        # if (
        #     rest_user.user_residential_district is not None
        #     and rest_user.user_residential_district != ""
        #     and rest_user.user_residential_district == user.user_residential_district
        # ) or (
        #     rest_user.user_nonresidential_city is not None
        #     and rest_user.user_nonresidential_city != ""
        #     and rest_user.user_nonresidential_city == user.user_nonresidential_city
        # ):
        #     if user.userid not in friendsuggestion.location:
        #         friendsuggestion.location.append(user.userid)

        #     if rest_user.userid not in user_friendsuggestion.location:
        #         user_friendsuggestion.location.append(rest_user.userid)

        # if rest_user.user_goal is not None and set(user_goal) & set(
        #     rest_user.user_goal
        # ):
        #     if user.userid not in friendsuggestion.goals:
        #         friendsuggestion.goals.append(user.userid)

        #     if rest_user.userid not in user_friendsuggestion.goals:
        #         user_friendsuggestion.goals.append(rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_goal", "goals", 'list')

        # if rest_user.user_interested_area is not None and set(
        #     user_interested_area
        # ) & set(rest_user.user_interested_area):
        #     if user.userid not in friendsuggestion.interest:
        #         friendsuggestion.interest.append(user.userid)

        #     if rest_user.userid not in user_friendsuggestion.interest:
        #         user_friendsuggestion.interest.append(rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_interested_area", "interest", 'list')

        # if (
        #     rest_user.user_durationyear_abroad is not None
        #     and rest_user.user_durationyear_abroad != ""
        #     and rest_user.user_durationyear_abroad == user.user_durationyear_abroad
        # ):
        #     if user.userid not in friendsuggestion.durationyear_abroad:
        #         friendsuggestion.durationyear_abroad.append(user.userid)

        #     if rest_user.userid not in user_friendsuggestion.durationyear_abroad:
        #         user_friendsuggestion.durationyear_abroad.append(
        #             rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_durationyear_abroad", "durationyear_abroad", 'string')

        # if (
        #     rest_user.user_current_location_durationyear is not None
        #     and rest_user.user_current_location_durationyear != ""
        #     and rest_user.user_current_location_durationyear
        #     == user.user_current_location_durationyear
        # ):
        #     if user.userid not in friendsuggestion.current_location_durationyear:
        #         friendsuggestion.current_location_durationyear.append(
        #             user.userid)

        #     if (
        #         rest_user.userid
        #         not in user_friendsuggestion.current_location_durationyear
        #     ):
        #         user_friendsuggestion.current_location_durationyear.append(
        #             rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_current_location_durationyear", "current_location_durationyear", 'string')

        # if (
        #     rest_user.user_industry is not None
        #     and rest_user.user_industry != ""
        #     and rest_user.user_industry == user.user_industry
        # ):
        #     if user.userid not in friendsuggestion.industry:
        #         friendsuggestion.industry.append(user.userid)
            
        #     if rest_user.userid not in user_friendsuggestion.industry:
        #         user_friendsuggestion.industry.append(rest_user.userid)
        
        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_industry", 'industry', 'string')

        # if (
        #     rest_user.user_areaof_experience is not None
        #     and rest_user.user_areaof_experience != ""
        #     and rest_user.user_areaof_experience == user.user_areaof_experience
        # ):
        #     if user.userid not in friendsuggestion.areaof_experience:
        #         friendsuggestion.areaof_experience.append(user.userid)
            
        #     if rest_user.userid not in user_friendsuggestion.areaof_experience:
        #         user_friendsuggestion.areaof_experience.append(
        #             rest_user.userid)
        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_areaof_experience", 'areaof_experience', 'string')
        # if (
        #     rest_user.user_industry_experienceyear is not None
        #     and rest_user.user_industry_experienceyear != ""
        #     and rest_user.user_industry_experienceyear
        #     == user.user_industry_experienceyear
        # ):
        #     if user.userid not in friendsuggestion.industry_experienceyear:
        #         friendsuggestion.industry_experienceyear.append(user.userid)
            
        #     if rest_user.userid not in user_friendsuggestion.industry_experienceyear:
        #         user_friendsuggestion.industry_experienceyear.append(
        #             rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_industry_experienceyear", 'industry_experienceyear', 'string')

        # if rest_user.is_user_serviceholder == user.is_user_serviceholder:
        #     if user.userid not in friendsuggestion.serviceholder:
        #         friendsuggestion.serviceholder.append(user.userid)

        #     if rest_user.userid not in user_friendsuggestion.serviceholder:
        #         user_friendsuggestion.serviceholder.append(rest_user.userid)
        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "is_user_serviceholder", 'serviceholder', 'bool')

        # if rest_user.is_user_selfemployed == user.is_user_selfemployed:
        #     if user.userid not in friendsuggestion.selfemployed:
        #         friendsuggestion.selfemployed.append(user.userid)

        #     if rest_user.userid not in user_friendsuggestion.selfemployed:
        #         user_friendsuggestion.selfemployed.append(rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "is_user_selfemployed", 'selfemployed', 'bool')

        # if (
        #     rest_user.user_currentdesignation is not None
        #     and rest_user.user_currentdesignation != ""
        #     and rest_user.user_currentdesignation == user.user_currentdesignation
        # ):
        #     if user.userid not in friendsuggestion.currentdesignation:
        #         friendsuggestion.currentdesignation.append(user.userid)
            
        #     if rest_user.userid not in user_friendsuggestion.currentdesignation:
        #         user_friendsuggestion.currentdesignation.append(
        #             rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_currentdesignation", 'currentdesignation', 'string')

        # if (
        #     rest_user.user_company_name is not None
        #     and rest_user.user_company_name != ""
        #     and rest_user.user_company_name == user.user_company_name
        # ):
        #     if user.userid not in friendsuggestion.company_name:
        #         friendsuggestion.company_name.append(user.userid)
        #     if rest_user.userid not in user_friendsuggestion.company_name:
        #         user_friendsuggestion.company_name.append(rest_user.userid)

        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_company_name", 'company_name', 'string')

        # if (
        #     rest_user.user_office_address is not None
        #     and rest_user.user_office_address != ""
        #     and rest_user.user_office_address == user.user_office_address
        # ):
        #     if user.userid not in friendsuggestion.office_address:
        #         friendsuggestion.office_address.append(user.userid)
        #     if rest_user.userid not in user_friendsuggestion.office_address:
        #         user_friendsuggestion.office_address.append(rest_user.userid)
        update_friendsuggestion(user, rest_user, user_friendsuggestion, friendsuggestion, "user_office_address", 'office_address', 'string')

        friendsuggestion.save()

    user_friendsuggestion.save()
