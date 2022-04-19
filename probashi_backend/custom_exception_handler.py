# from rest_framework.views import exception_handler


# def custom_exception_handler(exc, context):
#     # Call REST framework's default exception handler first,
#     # to get the standard error response.
#     response = exception_handler(exc, context)

#     print('response__handler:::::::',response)

#     if response is not None:
#         # check if exception has dict items
#         if hasattr(exc.detail, 'items'):
#             # remove the initial value
#             response.data = {}
#             errors = []
#             for key, value in exc.detail.items():
#                 # append errors into the list
#                 errors.append("{} : {}".format(key, " ".join(value)))
            
#             # add property errors to the response
#             response.data['errors'] = errors

#         # serve status code in the response
#         response.data['status_code'] = response.status_code
    
#     response_data = {'success': False, 'message': response}
#     return response_data



from rest_framework.views import exception_handler


def custom_exception_handler(exc):
    """
    Custom exception handler for Django Rest Framework that adds
    the `status_code` to the response and renames the `detail` key to `error`.
    """
    response = exception_handler(exc)

    if response is not None:
        # response.data['status_code'] = response.status_code
        response.data['success'] = False
        response.data['error'] = response.data['detail']
        del response.data['detail']

    return response



