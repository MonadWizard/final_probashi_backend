from auth_user_app.models import User
from .models import FriendsSuggation, UserFavouriteList
from django.db.models import Q
from asgiref.sync import sync_to_async


@sync_to_async
def match_friends(user_id):
    user = User.objects.get(userid=user_id)
    # print("userid:::::::::::::::::::::", user.userid)

    # print("user goal:::::::::::::::::::::", (user.user_goal))
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
        | Q(is_user_serviceholder=user.user_industry_experienceyear)
        | Q(is_user_selfemployed=user.is_user_selfemployed)
        | (
            Q(user_currentdesignation=user.user_currentdesignation)
            & Q(user_currentdesignation__isnull=False)
        )
        | (
            Q(user_company_name=user.user_company_name)
            & Q(user_company_name__isnull=False)
        )
        | (
            Q(user_office_address=user.user_office_address)
            & Q(user_office_address__isnull=False)
        )
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

    if user_friendsuggestion.durationyear_abroad is None:
        user_friendsuggestion.durationyear_abroad = []

    if user_friendsuggestion.current_location_durationyear is None:
        user_friendsuggestion.current_location_durationyear = []

    if user_friendsuggestion.industry is None:
        user_friendsuggestion.industry = []

    if user_friendsuggestion.areaof_experience is None:
        user_friendsuggestion.areaof_experience = []

    if user_friendsuggestion.industry_experienceyear is None:
        user_friendsuggestion.industry_experienceyear = []

    if user_friendsuggestion.serviceholder is None:
        user_friendsuggestion.serviceholder = []

    if user_friendsuggestion.selfemployed is None:
        user_friendsuggestion.selfemployed = []

    if user_friendsuggestion.currentdesignation is None:
        user_friendsuggestion.currentdesignation = []

    if user_friendsuggestion.company_name is None:
        user_friendsuggestion.company_name = []

    if user_friendsuggestion.office_address is None:
        user_friendsuggestion.office_address = []

    for rest_user in rest_users:
        try:
            friendsuggestion = FriendsSuggation.objects.get(user=rest_user.userid)
        except:
            friendsuggestion = FriendsSuggation.objects.create(user=rest_user)

        # if rest-user's residential districti is not null and same with user
        # then update this field in friendsuggestion

        if (
            rest_user.user_residential_district is not None
            and rest_user.user_residential_district != ""
            and rest_user.user_residential_district == user.user_residential_district
        ) or (
            rest_user.user_nonresidential_city is not None
            and rest_user.user_nonresidential_city != ""
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

        if (
            rest_user.user_durationyear_abroad is not None
            and rest_user.user_durationyear_abroad != ""
            and rest_user.user_durationyear_abroad == user.user_durationyear_abroad
        ):
            if friendsuggestion.durationyear_abroad is None:
                friendsuggestion.durationyear_abroad = []
            if user.userid not in friendsuggestion.durationyear_abroad:
                friendsuggestion.durationyear_abroad.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.durationyear_abroad:
                user_friendsuggestion.durationyear_abroad.append(rest_user.userid)

        if (
            rest_user.user_current_location_durationyear is not None
            and rest_user.user_current_location_durationyear != ""
            and rest_user.user_current_location_durationyear
            == user.user_current_location_durationyear
        ):
            if friendsuggestion.current_location_durationyear is None:
                friendsuggestion.current_location_durationyear = []
            if user.userid not in friendsuggestion.current_location_durationyear:
                friendsuggestion.current_location_durationyear.append(user.userid)
            if (
                rest_user.userid
                not in user_friendsuggestion.current_location_durationyear
            ):
                user_friendsuggestion.current_location_durationyear.append(
                    rest_user.userid
                )

        if (
            rest_user.user_industry is not None
            and rest_user.user_industry != ""
            and rest_user.user_industry == user.user_industry
        ):
            if friendsuggestion.industry is None:
                friendsuggestion.industry = []
            if user.userid not in friendsuggestion.industry:
                friendsuggestion.industry.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.industry:
                user_friendsuggestion.industry.append(rest_user.userid)

        if (
            rest_user.user_areaof_experience is not None
            and rest_user.user_areaof_experience != ""
            and rest_user.user_areaof_experience == user.user_areaof_experience
        ):
            if friendsuggestion.areaof_experience is None:
                friendsuggestion.areaof_experience = []
            if user.userid not in friendsuggestion.areaof_experience:
                friendsuggestion.areaof_experience.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.areaof_experience:
                user_friendsuggestion.areaof_experience.append(rest_user.userid)

        if (
            rest_user.user_industry_experienceyear is not None
            and rest_user.user_industry_experienceyear != ""
            and rest_user.user_industry_experienceyear
            == user.user_industry_experienceyear
        ):
            if friendsuggestion.industry_experienceyear is None:
                friendsuggestion.industry_experienceyear = []
            if user.userid not in friendsuggestion.industry_experienceyear:
                friendsuggestion.industry_experienceyear.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.industry_experienceyear:
                user_friendsuggestion.industry_experienceyear.append(rest_user.userid)

        if rest_user.is_user_serviceholder == user.is_user_serviceholder:
            if friendsuggestion.serviceholder is None:
                friendsuggestion.serviceholder = []
            if user.userid not in friendsuggestion.serviceholder:
                friendsuggestion.serviceholder.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.serviceholder:
                user_friendsuggestion.serviceholder.append(rest_user.userid)

        if rest_user.is_user_selfemployed == user.is_user_selfemployed:
            if friendsuggestion.selfemployed is None:
                friendsuggestion.selfemployed = []
            if user.userid not in friendsuggestion.selfemployed:
                friendsuggestion.selfemployed.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.selfemployed:
                user_friendsuggestion.selfemployed.append(rest_user.userid)

        if (
            rest_user.user_currentdesignation is not None
            and rest_user.user_currentdesignation != ""
            and rest_user.user_currentdesignation == user.user_currentdesignation
        ):
            if friendsuggestion.currentdesignation is None:
                friendsuggestion.currentdesignation = []
            if user.userid not in friendsuggestion.currentdesignation:
                friendsuggestion.currentdesignation.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.currentdesignation:
                user_friendsuggestion.currentdesignation.append(rest_user.userid)

        if (
            rest_user.user_company_name is not None
            and rest_user.user_company_name != ""
            and rest_user.user_company_name == user.user_company_name
        ):
            if friendsuggestion.company_name is None:
                friendsuggestion.company_name = []
            if user.userid not in friendsuggestion.company_name:
                friendsuggestion.company_name.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.company_name:
                user_friendsuggestion.company_name.append(rest_user.userid)

        if (
            rest_user.user_office_address is not None
            and rest_user.user_office_address != ""
            and rest_user.user_office_address == user.user_office_address
        ):
            if friendsuggestion.office_address is None:
                friendsuggestion.office_address = []
            if user.userid not in friendsuggestion.office_address:
                friendsuggestion.office_address.append(user.userid)
            if rest_user.userid not in user_friendsuggestion.office_address:
                user_friendsuggestion.office_address.append(rest_user.userid)

        friendsuggestion.save()

    user_friendsuggestion.save()
