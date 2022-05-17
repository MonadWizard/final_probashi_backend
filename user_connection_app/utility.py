from auth_user_app.models import User
from .models import FriendsSuggation, UserFavouriteList
from django.db.models import Q
from asgiref.sync import sync_to_async


@sync_to_async
def match_friends(user_id):
    user = User.objects.get(userid=user_id)
    print("userid:::::::::::::::::::::", user.userid)

    print("user goal:::::::::::::::::::::", (user.user_goal))
    user_goal = user.user_goal if user.user_goal else []
    user_interested_area = (
        user.user_interested_area if user.user_interested_area else []
    )
    queryset = User.objects.filter(
        (
            (
                Q(user_residential_district=user.user_residential_district)
                & Q(user_residential_district__isnull=False)
            )
            | (
                Q(user_nonresidential_city=user.user_nonresidential_city)
                & Q(user_nonresidential_city__isnull=False)
            )
            | Q(user_goal__contains=user_goal)
            | Q(user_interested_area__contains=user_interested_area)
        )
        & ~Q(userid=user_id)
        & Q(is_active=True)
        & ~Q(
            userid__in=UserFavouriteList.objects.filter(userid=user.userid).values(
                "userid"
            )
        )
        # | Q(user_durationyear_abroad=user.user_durationyear_abroad)
        # | Q(user_current_location_durationyear=user.user_current_location_durationyear)
        # | Q(user_industry=user.user_industry)
        # | Q(user_areaof_experience=user.user_areaof_experience)
        # | Q(user_industry_experienceyear=user.user_industry_experienceyear)
        # | Q(is_user_serviceholder=user.is_user_serviceholder)
        # | Q(is_user_selfemployed=user.is_user_selfemployed)
        # | Q(user_currentdesignation=user.user_currentdesignation)
        # | Q(user_company_name=user.user_company_name)
        # | Q(user_office_address=user.user_office_address)
    )
    print("rest_users:::::::::::::::::::::", queryset)
    rest_users = queryset.filter(~Q(userid=user_id))
    print("rest user:::::::::::", rest_users)

    try:
        user_friendsuggestion = FriendsSuggation.objects.get(user=user.userid)
    except:
        user_friendsuggestion = FriendsSuggation.objects.create(user=user)

    if user_friendsuggestion.location is None:
        user_friendsuggestion.location = []

    if user_friendsuggestion.goals is None:
        user_friendsuggestion.goals = []

    if user_friendsuggestion.interest is None:
        user_friendsuggestion.interest = []

    for rest_user in rest_users:
        try:
            friendsuggestion = FriendsSuggation.objects.get(user=rest_user.userid)
        except:
            friendsuggestion = FriendsSuggation.objects.create(user=rest_user)

        # if rest-user's residential districti is not null and same with user
        # then update this field in friendsuggestion

        if (
            rest_user.user_residential_district is not None
            and rest_user.user_residential_district == user.user_residential_district
        ) or (
            rest_user.user_nonresidential_city is not None
            and rest_user.user_nonresidential_city == user.user_nonresidential_city
        ):
            if friendsuggestion.location is None:
                friendsuggestion.location = []
            if user.userid not in friendsuggestion.location:
                friendsuggestion.location.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.location:
                user_friendsuggestion.location.append(rest_user.userid)

        if rest_user.user_goal is not None and set(user_goal) & set(
            rest_user.user_goal
        ):
            if friendsuggestion.goals is None:
                friendsuggestion.goals = []
            if user.userid not in friendsuggestion.goals:
                friendsuggestion.goals.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.goals:
                user_friendsuggestion.goals.append(rest_user.userid)

        if rest_user.user_interested_area is not None and set(
            user_interested_area
        ) & set(rest_user.user_interested_area):
            if friendsuggestion.interest is None:
                friendsuggestion.interest = []
            if user.userid not in friendsuggestion.interest:
                friendsuggestion.interest.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.interest:
                user_friendsuggestion.interest.append(rest_user.userid)

        friendsuggestion.save()

    user_friendsuggestion.save()
