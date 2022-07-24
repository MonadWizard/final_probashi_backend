import requests
import datetime
from .models import UserConsultAppointmentRequest, ConsultancyTimeSchudile


def Pro_user_CREATE_and_GET_session(request, user):

    current_time = datetime.datetime.now()
    current_time = current_time.strftime("%m%d%H%M%S%f")
    tran_id = current_time

    name = user.user_fullname
    email = user.user_email
    phone = user.user_callphone
    address = user.user_geolocation

    if user.user_email is not None:
        email = email
    else:
        email = "callphone@probashi.com"

    if user.user_residential_district is not None:
        country = "Bangladesh"
        city = f"{user.user_residential_district}"
    else:
        country = f"{user.user_nonresidential_country}"
        city = f"{user.user_nonresidential_city}"

    if user.user_callphone is not None:
        phone = phone
    else:
        phone = "+8800000000000"

    if address is None:
        address = "No Address Given"

    post_body = {}
    post_body["store_id"] = "Tripziplive"
    post_body["store_passwd"] = "5A9651E55CDAA86375"
    post_body["product_name"] = "become a pro"
    post_body["product_category"] = "paid user"
    post_body["product_profile"] = "premium"
    post_body["total_amount"] = "10"
    post_body["currency"] = "BDT"
    post_body[
        "success_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/pro-success/"
    post_body[
        "fail_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/pro-fail/"
    post_body[
        "cancel_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/pro-cancle/"

    post_body[
        "ipn_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/ipn-pro/"

    post_body["shipping_method"] = "NO"
    post_body["cus_name"] = name
    post_body["cus_email"] = email
    post_body["tran_id"] = tran_id
    post_body["cus_add1"] = address
    post_body["cus_city"] = city
    post_body["cus_country"] = country
    post_body["cus_phone"] = phone

    sslcommerz_api_url = "https://securepay.sslcommerz.com/gwprocess/v4/api.php"
    res = requests.post(sslcommerz_api_url, post_body)
    resp = {"res": res.json(), "post_body": post_body}
    return resp


def Consultancy_CREATE_and_GET_session(request, user):

    current_time = datetime.datetime.now()
    current_time = current_time.strftime("%m%d%H%M%S%f")


    tran_id = current_time
    name = user.user_fullname
    email = user.user_email
    phone = user.user_callphone
    address = user.user_geolocation

    consultancy = ConsultancyTimeSchudile.objects.filter(
        id=request.data["ConsultancyTimeSchudile"]
    ).values(
        "consultancyid__consultant_name",
        "consultancy_rate",
        "consultancyid__consultant_service_category",
    )

    consultancy_name = consultancy[0]["consultancyid__consultant_name"]
    consultancy_amount = consultancy[0]["consultancy_rate"]
    consultancy_category = consultancy[0]["consultancyid__consultant_service_category"]

    if email is None:
        email = "callphone@probashi.com"

    if phone is None:
        phone = "+880000000000"

    if address is None:
        address = "No Address Given"

    if user.user_residential_district is not None:
        country = "Bangladesh"
        city = f"{user.user_residential_district}"
    else:
        country = f"{user.user_nonresidential_country}"
        city = f"{user.user_nonresidential_city}"

    post_body = {}
    post_body["store_id"] = "Tripziplive"
    post_body["store_passwd"] = "5A9651E55CDAA86375"
    post_body["product_name"] = consultancy_name
    post_body["product_category"] = consultancy_category
    post_body["product_profile"] = "counsultancy"
    post_body["total_amount"] = consultancy_amount
    post_body["currency"] = "BDT"
    post_body["cus_name"] = name
    post_body["cus_email"] = email
    post_body["cus_phone"] = phone
    post_body["cus_add1"] = address
    post_body["cus_city"] = city
    post_body["cus_country"] = country
    post_body["tran_id"] = tran_id

    post_body[
        "success_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/consultancy-success/"
    post_body[
        "fail_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/consultancy-fail/"
    post_body[
        "cancel_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/consultancy-cancle/"

    post_body[
        "ipn_url"
    ] = "https://probashiapi.algorithmgeneration.com/consultancy/ipn/"

    post_body["shipping_method"] = "NO"

    sslcommerz_api_url = "https://securepay.sslcommerz.com/gwprocess/v4/api.php"
    res = requests.post(sslcommerz_api_url, post_body)
    resp = {"res": res.json(), "post_body": post_body}
    return resp


def orderVerify(request):
    val_id = request.data["val_id"]
    store_id = request.data["store_id"]
    store_passwd = "5A9651E55CDAA86375"
    external_api_url = (
        "https://securepay.sslcommerz.com/validator/api/validationserverAPI.php?val_id="
        + val_id
        + "&store_id="
        + store_id
        + "&store_passwd="
        + store_passwd
        + "&format=json"
    )
    res = requests.get(external_api_url)
    return res.json()
