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


def append_item_in_list(
    user_obj,
    rest_obj,
    user_friend_suggestion_obj,
    rest_friend_suggestion_obj,
    friend_suggestion_attribute,
):

    rest_values = getattr(rest_friend_suggestion_obj, friend_suggestion_attribute)
    user_values = getattr(user_friend_suggestion_obj, friend_suggestion_attribute)

    if user_obj.userid not in rest_values:
        rest_values.append(user_obj.userid)

    if rest_obj.userid not in user_values:
        user_values.append(rest_obj.userid)


def update_friendsuggestion(
    user_obj,
    rest_obj,
    user_friend_suggestion_obj,
    rest_friend_suggestion_obj,
    user_attribute,
    friend_suggestion_attribute,
    type,
):
    if type == "string":
        if (
            getattr(rest_obj, user_attribute) is not None
            and getattr(rest_obj, user_attribute) != ""
            and getattr(rest_obj, user_attribute) == getattr(user_obj, user_attribute)
        ):
            append_item_in_list(
                user_obj,
                rest_obj,
                user_friend_suggestion_obj,
                rest_friend_suggestion_obj,
                friend_suggestion_attribute,
            )

    elif type == "list":
        if getattr(rest_obj, user_attribute) is not None and (
            set(getattr(rest_obj, user_attribute))
            & set(getattr(user_obj, user_attribute))
        ):

            append_item_in_list(
                user_obj,
                rest_obj,
                user_friend_suggestion_obj,
                rest_friend_suggestion_obj,
                friend_suggestion_attribute,
            )

    elif type == "bool":
        if getattr(rest_obj, user_attribute) == getattr(user_obj, user_attribute):
            append_item_in_list(
                user_obj,
                rest_obj,
                user_friend_suggestion_obj,
                rest_friend_suggestion_obj,
                friend_suggestion_attribute,
            )
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
        & ~Q(userid=user_id)
        & Q(is_active=True)
        & ~Q(is_staff=True)
        & ~Q(
            userid__in=UserFavouriteList.objects.filter(userid=user.userid).values(
                "userid"
            )
        )
    )

    user_friendsuggestion = get_or_create_friend_suggestion(user)

    attributes = [
        {
            "attribute": "user_residential_district",
            "type": "string",
            "friend_suggestion_attribute": "location",
        },
        {
            "attribute": "user_nonresidential_city",
            "type": "string",
            "friend_suggestion_attribute": "location",
        },
        {
            "attribute": "user_goal",
            "type": "list",
            "friend_suggestion_attribute": "goals",
        },
        {
            "attribute": "user_interested_area",
            "type": "list",
            "friend_suggestion_attribute": "interest",
        },
        {
            "attribute": "user_durationyear_abroad",
            "type": "string",
            "friend_suggestion_attribute": "durationyear_abroad",
        },
        {
            "attribute": "user_current_location_durationyear",
            "type": "string",
            "friend_suggestion_attribute": "current_location_durationyear",
        },
        {
            "attribute": "user_industry",
            "type": "string",
            "friend_suggestion_attribute": "industry",
        },
        {
            "attribute": "user_areaof_experience",
            "type": "string",
            "friend_suggestion_attribute": "areaof_experience",
        },
        {
            "attribute": "user_industry_experienceyear",
            "type": "string",
            "friend_suggestion_attribute": "industry_experienceyear",
        },
        {
            "attribute": "is_user_serviceholder",
            "type": "bool",
            "friend_suggestion_attribute": "serviceholder",
        },
        {
            "attribute": "is_user_selfemployed",
            "type": "bool",
            "friend_suggestion_attribute": "selfemployed",
        },
        {
            "attribute": "user_currentdesignation",
            "type": "string",
            "friend_suggestion_attribute": "currentdesignation",
        },
        {
            "attribute": "user_company_name",
            "type": "string",
            "friend_suggestion_attribute": "company_name",
        },
        {
            "attribute": "user_office_address",
            "type": "string",
            "friend_suggestion_attribute": "office_address",
        }
    ]

    for rest_user in rest_users:
        friendsuggestion = get_or_create_friend_suggestion(rest_user)
        for attribute in attributes:
            update_friendsuggestion(
                user,
                rest_user,
                user_friendsuggestion,
                friendsuggestion,
                attribute["attribute"],
                attribute["friend_suggestion_attribute"],
                attribute["type"],
            )


        friendsuggestion.save()

    user_friendsuggestion.save()
