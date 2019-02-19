import dl.contract

USERS_FILES_PATH = "data/users/"
USER_FILES_LIMIT = 5
# To disallow XSS attacks - allowed extensions limitation
ALLOWED_EXTENSIONS_ENABLED = True
ALLOWED_EXTENSIONS = dl.contract.ALLOWED_FILES_EXTENSIONS
#APP_MAIN_ENDPOINT = '/milewsp1/app/'
#APP_ADDRESS = "https://pi.iem.pw.edu.pl/" + APP_MAIN_ENDPOINT TODO<CONF>: Set it back
APP_MAIN_ENDPOINT = '/'
APP_ADDRESS = "http://localhost:" + "5001" + APP_MAIN_ENDPOINT
ENDPOINTS_ADDRESSES = {
    "upload": APP_ADDRESS + "upload",
    "download": APP_ADDRESS + "download/"
}
JWT_KEY = "USED_SECRET"
