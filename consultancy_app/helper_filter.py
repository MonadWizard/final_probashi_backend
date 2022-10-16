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
        return queryset.filter(educationService_degree__overlap=value)
    else:
        return queryset


def filterby_consultant_servicebudget_startrange__gt(queryset, value):
    if value:
        return queryset.filter(consultant_servicebudget_startrange__gte=value)
    else:
        return queryset


def filterby_consultant_servicebudget_endrange__lt(queryset, value):
    if value:
        return queryset.filter(consultant_servicebudget_endrange__lte=value)
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
        return queryset.filter(digitalservice_type__overlap=value)
    else:
        return queryset


#
def filterby_legalcivilservice_required(queryset, value):
    if value:
        return queryset.filter(legalcivilservice_required__overlap=value)
    else:
        return queryset


def filterby_legalcivilservice_issued(queryset, value):
    if value:
        return queryset.filter(legalcivilservice_issue__overlap=value)
    else:
        return queryset


def filterby_medicalconsultancyservice_treatment_area(queryset, value):
    if value:
        # print("filterby_medicalconsultancyservice_treatment_area", queryset.filter(medicalconsultancyservice_treatment_area__in=value))
        return queryset.filter(medicalconsultancyservice_treatment_area__overlap=value)
        
    else:
        return queryset


def filterby_overseasrecruitmentservice_job_type(queryset, value):
    if value:
        return queryset.filter(overseasrecruitmentservice_job_type__overlap=value)
    else:
        return queryset


def filterby_propertymanagementservice_propertylocation(queryset, value):
    if value:
        return queryset.filter(propertymanagementservice_propertylocation=value)
    else:
        return queryset


def filterby_propertymanagementservice_type(queryset, value):
    if value:
        return queryset.filter(propertymanagementservice_type__overlap=value)
    else:
        return queryset


def filterby_propertymanagementservice_need(queryset, value):
    if value:
        return queryset.filter(propertymanagementservice_need__overlap=value)
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
        return queryset.filter(tourismservices__overlap=value)
    else:
        return queryset


def filterby_tradefacilitationservice_type(queryset, value):
    if value:
        return queryset.filter(tradefacilitationservice_type__overlap=value)
    else:
        return queryset


def filterby_tradefacilitationservice_Purpose(queryset, value):
    if value:
        return queryset.filter(tradefacilitationservice_Purpose__overlap=value)
    else:
        return queryset


def filterby_trainingservice_topic(queryset, value):
    if value:
        return queryset.filter(trainingservice_topic__overlap=value)
    else:
        return queryset


def filterby_trainingservice_duration(queryset, value):
    if value:
        return queryset.filter(trainingservice_duration__overlap=value)
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
