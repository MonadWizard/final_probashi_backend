from re import A
from auth_user_app.models import User
from .models import FriendsSuggation
from django.db.models import Q
from asgiref.sync import sync_to_async


# def insert_user(friendsuggestion, rest_user, user):
#     # locations = []
#     # goals = []
#     # interests = []
#     user_goals = user.user_goal if user.user_goal else []
#     user_interested_area = (
#         user.user_interested_area if user.user_interested_area else []
#     )
#     rest_user_goals = rest_user.user_goal if rest_user.user_goal else []
#     rest_user_interested_area = (
#         rest_user.user_interested_area if rest_user.user_interested_area else []
#     )
#     if friendsuggestion.location is None:
#         friendsuggestion.location = []
#         friendsuggestion.location.append(user.userid)
#         # friendsuggestion.location = "{" + str(user.userid) + "}"
#         # print("friendsuggation:::::::", friendsuggestion.location)
#     else:
#         if (user.user_residential_district == rest_user.user_residential_district) or (
#             user.user_nonresidential_country == rest_user.user_nonresidential_country
#         ):
#             friendsuggestion.location.append(rest_user.userid)

#     if friendsuggestion.goals is None:
#         # friendsuggestion.goals = "{" + str(user.userid) + "}"
#         friendsuggestion.goals = []
#         friendsuggestion.goals.append(user.userid)
#     else:
#         if set(user_goals) & set(rest_user_goals):
#             friendsuggestion.goals.append(rest_user.userid)

#     if friendsuggestion.interest is None:
#         # friendsuggestion.interest = "{" + str(user.userid) + "}"
#         friendsuggestion.interest = []
#         friendsuggestion.interest.append(user.userid)
#     else:
#         if set(user_interested_area) & set(rest_user_interested_area):
#             friendsuggestion.interest.append(rest_user.userid)

#     friendsuggestion.save()

#     print("friendsuggation:::::::", friendsuggestion.location)


# # @sync_to_async
# def match_friends(user_id):
#     user = User.objects.get(userid=user_id)
#     print("userid:::::::::::::::::::::", user.userid)

#     print("user goal:::::::::::::::::::::", (user.user_goal))
#     user_goal = user.user_goal if user.user_goal else []
#     user_interested_area = (
#         user.user_interested_area if user.user_interested_area else []
#     )
#     queryset = User.objects.filter(
#         Q(user_residential_district=user.user_residential_district)
#         | Q(user_nonresidential_city=user.user_nonresidential_city)
#         | Q(user_goal__in=user_goal)
#         | Q(user_interested_area__in=user_interested_area)
#     )
#     print("rest_users:::::::::::::::::::::", queryset)
#     rest_users = queryset.filter(~Q(userid=user_id))
#     print("rest user:::::::::::", rest_users)

#     for rest_user in rest_users:
#         try:
#             friendsuggestion = FriendsSuggation.objects.get(user=rest_user.userid)
#         except:
#             friendsuggestion = FriendsSuggation.objects.create(user=rest_user)

#         # .......................................................
#         insert_user(friendsuggestion, rest_user, user)


def match_friends(user_id):
    user = User.objects.get(userid=user_id)
    rest_users = User.objects.filter(~Q(userid=user_id))

    # residential location (division of BD), country Bangladesh fixed
    # non-residential location (specific country, specific city)
    # print("================")
    # print(user, user.user_email)
    # run a loop in rest users
    # match location with user
    # match goals with user
    # match interests with user
    # update friend suggestion model
    locations = []
    goals = []
    interests = []

    for rest_user in rest_users:
        if (
            user.user_residential_district is not None
            and rest_user.user_residential_district is not None
        ):
            if user.user_residential_district == rest_user.user_residential_district:
                try:
                    friendsuggestion = FriendsSuggation.objects.get(
                        user=rest_user.userid
                    )
                except:
                    friendsuggestion = FriendsSuggation.objects.create(user=rest_user)

                if friendsuggestion.location is None:
                    friendsuggestion.location = "{" + str(user.userid) + "}"
                else:
                    friendsuggestion.location.append(user.userid)

                friendsuggestion.save()
                locations.append(rest_user.userid)

        if (
            user.user_nonresidential_country is not None
            and rest_user.user_nonresidential_country is not None
        ):
            if (
                user.user_nonresidential_country
                == rest_user.user_nonresidential_country
            ):
                try:
                    friendsuggestion = FriendsSuggation.objects.get(
                        user=rest_user.userid
                    )
                except:
                    friendsuggestion = FriendsSuggation.objects.create(user=rest_user)

                if friendsuggestion.location is None:
                    friendsuggestion.location = "{" + str(user.userid) + "}"
                else:
                    friendsuggestion.location.append(user.userid)

                friendsuggestion.save()
                locations.append(rest_user.userid)

        if user.user_goal is not None and rest_user.user_goal is not None:
            for g in user.user_goal:
                for rg in rest_user.user_goal:
                    if g == rg:
                        try:
                            friendsuggestion = FriendsSuggation.objects.get(
                                user=rest_user.userid
                            )
                        except:
                            friendsuggestion = FriendsSuggation.objects.create(
                                user=rest_user
                            )

                        if friendsuggestion.goals is None:
                            friendsuggestion.goals = "{" + str(user.userid) + "}"
                        else:
                            friendsuggestion.goals.append(user.userid)

                        friendsuggestion.save()
                        print(user, rest_user, "goals")
                        goals.append(rest_user.userid)

        if (
            user.user_interested_area is not None
            and rest_user.user_interested_area is not None
        ):
            for i in user.user_interested_area:
                for ri in rest_user.user_interested_area:
                    if i == ri:
                        try:
                            friendsuggestion = FriendsSuggation.objects.get(
                                user=rest_user.userid
                            )
                        except:
                            friendsuggestion = FriendsSuggation.objects.create(
                                user=rest_user
                            )

                        # print(friendsuggestion.interest)
                        if friendsuggestion.interest is None:
                            friendsuggestion.interest = "{" + str(user.userid) + "}"
                        else:
                            friendsuggestion.interest.append(user.userid)

                        friendsuggestion.save()
                        interests.append(rest_user.userid)

    try:
        friendsuggestion = FriendsSuggation.objects.get(user=user_id)
    except:
        user = User.objects.get(userid=user_id)
        friendsuggestion = FriendsSuggation.objects.create(user=user)

    if len(locations) > 0:
        friendsuggestion.location = locations

    if len(goals) > 0:
        friendsuggestion.goals = goals

    if len(interests) > 0:
        friendsuggestion.interest = interests

    friendsuggestion.save()
