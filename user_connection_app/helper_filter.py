def filterby_userEduDegree(queryset, value):
    if value:
        return queryset.filter(user_edu_degree__in=value)
    else:
        return queryset



def filterby_userIndustry(queryset, value):
    if value:
        return queryset.filter(user_industry__in=value)
    else:
        return queryset

def filterby_residentialDistrict(queryset, value):
    if value:
        return queryset.filter(user_residential_district__in=value)
    else:
        return queryset

def filterby_nonresidentialCity(queryset, value):
    if value:
        return queryset.filter(user_nonresidential_city__in=value)
    else:
        return queryset




def filterby_consultantServiceCategory(queryset, value):
    if value:
        return queryset.filter(consultant_service_category__in=value)
    else:
        return queryset
