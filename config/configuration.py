from authorization.tools import hash_string

SESSION_KEY = hash_string("PyAppForClasses")
USERS_FILES_PATH = "data/users/"
USER_FILES_LIMIT = 5
# To disallow XSS attacks - allowed extensions limitation
ALLOWED_EXTENSIONS_ENABLED = True
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
SERVER_FULL_ADDRESS = "https://pi.iem.pw.edu.pl/milewsp1/app/"
ENDPOINTS_ADDRESSES = {
    "upload" : SERVER_FULL_ADDRESS + "upload",
    "download" : SERVER_FULL_ADDRESS + "download",
    "dashboard" : SERVER_FULL_ADDRESS + "dashboard",
    "logout" : SERVER_FULL_ADDRESS + "logout",
    "login": SERVER_FULL_ADDRESS + "login"
}
