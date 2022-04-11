from auth_user_app.models import User
from auth_user_app.models import FriendSuggation
from django.db.models import Q

def match_friends(user_id):
    user = User.objects.get(userid=user_id)
    rest_users = User.objects.filter(~Q(userid=user_id))

    # residential location (division of BD), country Bangladesh fixed
    # non-residential location (specific country, specific city)
    print("================")
    print(user, user.user_residential_district)
    print("================")
    print("\n")
    # run a loop in rest users
    # match location with user
    # match goals with user
    # match interests with user
    # update friend suggestion model
    locations = []

    for rest_user in rest_users:
        if user.user_residential_district is not None and rest_user.user_residential_district is not None:
            if user.user_residential_district == rest_user.user_residential_district:
                locations.append(rest_user.userid)
        
        if user.user_nonresidential_country is not None and rest_user.user_nonresidential_country is not None:
            if user.user_nonresidential_country == rest_user.user_nonresidential_country:
                locations.append(rest_user.userid)
    
    # print(locations)
    try:
        friendsuggestion = FriendSuggation.objects.get(user=user_id)
    except:
        user = User.objects.get(userid=user_id)
        friendsuggestion = FriendSuggation.objects.create(user=user)
    
    if len(locations) > 0:
        friendsuggestion.localtion = locations
    
    friendsuggestion.save()