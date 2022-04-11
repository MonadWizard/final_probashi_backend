from re import A
from auth_user_app.models import User
from auth_user_app.models import FriendSuggation
from django.db.models import Q

def match_friends(user_id):
    user = User.objects.get(userid=user_id)
    rest_users = User.objects.filter(~Q(userid=user_id))

    # residential location (division of BD), country Bangladesh fixed
    # non-residential location (specific country, specific city)
    print("================")
    print(user, user.user_email)
    # run a loop in rest users
    # match location with user
    # match goals with user
    # match interests with user
    # update friend suggestion model
    locations = []
    goals = []
    interests = []

    for rest_user in rest_users:
        if user.user_residential_district is not None and rest_user.user_residential_district is not None:
            if user.user_residential_district == rest_user.user_residential_district:
                try:
                    friendsuggestion = FriendSuggation.objects.get(user=rest_user.userid)
                except:
                    friendsuggestion = FriendSuggation.objects.create(user=rest_user)
                    
                if friendsuggestion.location is None:
                    friendsuggestion.location = "{" + str(user.userid) + "}"
                else:
                    friendsuggestion.location.append(user.userid)
                
                friendsuggestion.save()
                locations.append(rest_user.userid)
        
        if user.user_nonresidential_country is not None and rest_user.user_nonresidential_country is not None:
            if user.user_nonresidential_country == rest_user.user_nonresidential_country:
                try:
                    friendsuggestion = FriendSuggation.objects.get(user=rest_user.userid)
                except:
                    friendsuggestion = FriendSuggation.objects.create(user=rest_user)
                    
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
                            friendsuggestion = FriendSuggation.objects.get(user=rest_user.userid)
                        except:
                            friendsuggestion = FriendSuggation.objects.create(user=rest_user)
                            
                        if friendsuggestion.goals is None:
                            friendsuggestion.goals = "{" + str(user.userid) + "}"
                        else:
                            friendsuggestion.goals.append(user.userid)
                        
                        friendsuggestion.save()
                        print(user, rest_user, "goals")
                        goals.append(rest_user.userid)
        
        if user.user_interested_area is not None and rest_user.user_interested_area is not None:
            for i in user.user_interested_area:
                for ri in rest_user.user_interested_area:
                    if i == ri:
                        try:
                            friendsuggestion = FriendSuggation.objects.get(user=rest_user.userid)
                        except:
                            friendsuggestion = FriendSuggation.objects.create(user=rest_user)
                        
                        # print(friendsuggestion.interest)
                        if friendsuggestion.interest is None:
                            friendsuggestion.interest = "{" + str(user.userid) + "}"
                        else:
                            friendsuggestion.interest.append(user.userid)
                        
                        friendsuggestion.save()
                        interests.append(rest_user.userid)
                        
    try:
        friendsuggestion = FriendSuggation.objects.get(user=user_id)
    except:
        user = User.objects.get(userid=user_id)
        friendsuggestion = FriendSuggation.objects.create(user=user)
    
    if len(locations) > 0:
        friendsuggestion.location = locations
    
    if len(goals) > 0:
        friendsuggestion.goals = goals
    
    if len(interests) > 0:
        friendsuggestion.interest = interests
    
    friendsuggestion.save()