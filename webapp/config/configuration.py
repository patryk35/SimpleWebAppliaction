SSL_CERTIFICATE_VERIFY = False
APP_MAIN_ENDPOINT = "/milewsp1/app/"
APP_ADDRESS = "" #ADRESS_STRING

ENDPOINTS_RELATIVE_ADDRESSES = {
    "dashboard": APP_MAIN_ENDPOINT + "dashboard",
    "logout": APP_MAIN_ENDPOINT + "logout",
    "login": APP_MAIN_ENDPOINT + "login",
    "login_auth": APP_MAIN_ENDPOINT + "login_auth",
    "upload": APP_MAIN_ENDPOINT + "upload",
    "share": APP_MAIN_ENDPOINT + "share",
    "show_file_link": APP_MAIN_ENDPOINT + "show_link",
    "long_polling_notify": APP_MAIN_ENDPOINT + "long_polling_notify",
    "polling_data": APP_MAIN_ENDPOINT + "polling_data",
    "callback": APP_MAIN_ENDPOINT + 'callback'
}

ENDPOINTS_FULL_ADDRESSES = {
    "dashboard": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["dashboard"],
    "logout": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["logout"],
    "login": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["login"],
    "login_auth": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["login_auth"],
    "upload": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["upload"],
    "share": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["share"],
    "show_file_link": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["show_file_link"],
    "long_polling_notify": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["long_polling_notify"],
    "polling_data": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["polling_data"],
    "callback": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES['callback']
}

