def error_return_message(error_message):
    data = ""
    if "userid" in error_message:
        data += "user id is invalid"
    if "username" in error_message:
        data += "username is invalid"
    return data
