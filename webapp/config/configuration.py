from webapp.authorization.tools import hash_string

SESSION_KEY = hash_string("PyAppForClasses")
JWT_SECRET_KEY = "USED_SECRET"
#APP_MAIN_ENDPOINT = "/milewsp1/webapp/"
#APP_ADDRESS = "http://pi.iem.pw.edu.pl" + APP_MAIN_ENDPOINT TODO<CONF>: Set it back
APP_MAIN_ENDPOINT="/"
APP_ADDRESS = "http://localhost:5000" + APP_MAIN_ENDPOINT
ENDPOINTS_ADDRESSES = {
    "dashboard": APP_ADDRESS + "dashboard",
    "logout": APP_ADDRESS + "logout",
    "login": APP_ADDRESS + "login",
    "upload": APP_ADDRESS + "upload",
    "download": APP_ADDRESS + "download"
}
JWT_KEY = "USED_SECRET"
