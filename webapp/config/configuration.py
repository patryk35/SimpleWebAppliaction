SSL_CERTIFICATE_VERIFY = False
APP_MAIN_ENDPOINT = "/milewsp1/app/"
APP_STATIC = "/~milewsp1/static/"
APP_ADDRESS = "https://*SECRET*"

ENDPOINTS_RELATIVE_ADDRESSES = {
    "dashboard": APP_MAIN_ENDPOINT + "dashboard",
    "authorization": APP_MAIN_ENDPOINT + "authorization",
    "logout": APP_MAIN_ENDPOINT + "logout",
    "login_auth": APP_MAIN_ENDPOINT + "login_auth",
    "upload_endpoint": APP_MAIN_ENDPOINT + "uploadfile",
    "upload_site": APP_MAIN_ENDPOINT + "upload",
    "share": APP_MAIN_ENDPOINT + "share",
    "show_file_link": APP_MAIN_ENDPOINT + "show_link",
    "long_polling_notify": APP_MAIN_ENDPOINT + "long_polling_notify",
    "polling_data": APP_MAIN_ENDPOINT + "polling_data",
    "callback": APP_MAIN_ENDPOINT + 'callback'
}

ENDPOINTS_FULL_ADDRESSES = {
    "dashboard": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["dashboard"],
    "authorization": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["authorization"],
    "login_auth": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["login_auth"],
    "logout": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["logout"],
    "upload_endpoint": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["upload_endpoint"],
    "upload_site": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["upload_site"],
    "share": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["share"],
    "show_file_link": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["show_file_link"],
    "long_polling_notify": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["long_polling_notify"],
    "polling_data": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["polling_data"],
    "callback": APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES['callback']
}

LAYOUT_PARAMETERS = {
    'jquery_path': APP_ADDRESS + APP_STATIC + "js/jquery/jquery.min.js",
    'bundle_path': APP_ADDRESS + APP_STATIC + "css/bootstrap/js/bootstrap.bundle.min.js",
    'bootstrap_css': APP_ADDRESS + APP_STATIC + "css/bootstrap/css/bootstrap.min.css",
    'my_css': APP_ADDRESS + APP_STATIC + "css/main.css",
    'authorization_endpoint': APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["authorization"],
    'dashboard_endpoint': APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["dashboard"],
    'upload_endpoint': APP_ADDRESS + ENDPOINTS_RELATIVE_ADDRESSES["upload_site"],
}

LONG_POLLING_JS_FILE = APP_ADDRESS + APP_STATIC + "js/longpolling.js"
