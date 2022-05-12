def filterby_consultant_service_category(model, value):
    if value:
        return model.objects.filter(consultant_service_category=value)
    else:
        return model.objects.all()


def filterby_consultant_service_locationcountry(queryset, value):
    if value:
        return queryset.filter(consultant_service_locationcountry=value)
    else:
        return queryset


def filterby_educationService_degree(queryset, value):
    if value:
        return queryset.filter(educationService_degree=value)
    else:
        return queryset


def filterby_consultant_servicebudget_startrange__gt(queryset, value):
    if value:
        return queryset.filter(consultant_servicebudget_startrange__gt=value)
    else:
        return queryset


def filterby_consultant_servicebudget_endrange__lt(queryset, value):
    if value:
        return queryset.filter(consultant_servicebudget_endrange__lt=value)
    else:
        return queryset


# Digital
def filterby_is_userconsultant_personal(queryset, value):
    if value:
        return queryset.filter(is_userconsultant_personal=value)
    else:
        return queryset


def filterby_is_userconsultant_company(queryset, value):
    if value:
        return queryset.filter(is_userconsultant_company=value)
    else:
        return queryset


def filterby_digitalservice_type(queryset, value):
    if value:
        return queryset.filter(digitalservice_type=value)
    else:
        return queryset


#
def filterby_legalcivilservice_required(queryset, value):
    if value:
        return queryset.filter(legalcivilservice_required=value)
    else:
        return queryset


def filterby_legalcivilservice_issued(queryset, value):
    if value:
        return queryset.filter(legalcivilservice_issue=value)
    else:
        return queryset


def filterby_medicalconsultancyservice_treatment_area(queryset, value):
    if value:
        return queryset.filter(medicalconsultancyservice_treatment_area=value)
    else:
        return queryset


def filterby_overseasrecruitmentservice_job_type(queryset, value):
    if value:
        return queryset.filter(overseasrecruitmentservice_job_type=value)
    else:
        return queryset


def filterby_propertymanagementservice_propertylocation(queryset, value):
    if value:
        return queryset.filter(propertymanagementservice_propertylocation=value)
    else:
        return queryset


def filterby_propertymanagementservice_type(queryset, value):
    if value:
        return queryset.filter(propertymanagementservice_type=value)
    else:
        return queryset


def filterby_propertymanagementservice_need(queryset, value):
    if value:
        return queryset.filter(propertymanagementservice_need=value)
    else:
        return queryset


# Tourism
def filterby_is_userconsultant_company(queryset, value):
    if value:
        return queryset.filter(is_userconsultant_company=value)
    else:
        return queryset


def filterby_tourismservices(queryset, value):
    if value:
        return queryset.filter(tourismservices=value)
    else:
        return queryset


def filterby_tradefacilitationservice_type(queryset, value):
    if value:
        return queryset.filter(tradefacilitationservice_type=value)
    else:
        return queryset


def filterby_tradefacilitationservice_Purpose(queryset, value):
    if value:
        return queryset.filter(tradefacilitationservice_Purpose=value)
    else:
        return queryset


def filterby_trainingservice_topic(queryset, value):
    if value:
        return queryset.filter(trainingservice_topic=value)
    else:
        return queryset


def filterby_trainingservice_duration(queryset, value):
    if value:
        return queryset.filter(trainingservice_duration=value)
    else:
        return queryset


def filterby_multiple_service(queryset, value):
    if value:
        return queryset.filter(consultant_service_category__in=value)
    else:
        return queryset


def filterby_multiple_location(queryset, value):
    if value:
        return queryset.filter(consultant_service_locationcountry__in=value)
    else:
        return queryset
