APP_MAIN_ENDPOINT = '/milewsp1/file/'
APP_ADDRESS = "https://*SECRET*/"

USERS_FILES_PATH = "data/users/"
USER_FILES_LIMIT = 5
# To disallow XSS attacks - allowed extensions limitation
ALLOWED_EXTENSIONS_ENABLED = True
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

ENDPOINTS_RELATIVE_ADDRESSES = {
    "upload": APP_MAIN_ENDPOINT + "upload",
    "download": APP_MAIN_ENDPOINT + "download",
    "files": APP_MAIN_ENDPOINT + "files",
    "share": APP_MAIN_ENDPOINT + "share"
}

ENDPOINTS_FULL_ADDRESSES = {
    "upload": ENDPOINTS_RELATIVE_ADDRESSES["upload"],
    "download": ENDPOINTS_RELATIVE_ADDRESSES["download"],
    "files": ENDPOINTS_RELATIVE_ADDRESSES["files"],
    "share": ENDPOINTS_RELATIVE_ADDRESSES["share"]
}
