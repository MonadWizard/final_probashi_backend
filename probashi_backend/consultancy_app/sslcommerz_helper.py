import requests
import datetime 


def Pro_user_CREATE_and_GET_session(request, user):

    current_time = datetime.datetime.now() 
    current_time = current_time.strftime("%m%d%H%M%S%f")
    tran_id = current_time

    if user.user_email is not None:
        email = user.user_email
    else:
        email = 'callphone@probashi.com'

    if user.user_residential_district is not None:
        country = 'Bangladesh'
        city = f'{user.user_residential_district}'
    else:
        country = f'{user.user_nonresidential_country}'
        city = f'{user.user_nonresidential_city}'

    if user.user_callphone is not None:
        phone = user.user_callphone
    else:
        phone = '+8801711123456'

    post_body = {}
    post_body['store_id'] = 'mworg624bb703abfce'
    post_body['store_passwd'] = 'mworg624bb703abfce@ssl'
    post_body['product_name'] = 'become a pro'
    post_body['product_category'] = 'paid user'
    post_body['product_profile'] = 'premium'
    post_body['total_amount'] = '100'
    post_body['currency'] = 'BDT'
    post_body['success_url'] = 'https://www.py-bangla.pagla.me/&'
    post_body['fail_url'] = 'https://www.py-bangla.pagla.me/&'
    post_body['cancel_url']= 'https://www.py-bangla.pagla.me/&'
    post_body['cus_name'] = f'{user.user_fullname}'
    post_body['cus_email'] = f'{email}'
    post_body['tran_id'] = f'{tran_id}'
    post_body['cus_add1'] = f'{user.user_geolocation}'
    post_body['cus_city'] = f'{city}'
    post_body['cus_country'] = f'{country}'
    post_body['cus_phone'] = f'{phone}'
    post_body['shipping_method'] = 'NO'


    sslcommerz_api_url = 'https://sandbox.sslcommerz.com/gwprocess/v4/api.php' 
    res = requests.post(sslcommerz_api_url, post_body)
    # print("::::::::", res)
    return res.json()
