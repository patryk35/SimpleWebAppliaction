APP_MAIN_ENDPOINT = '/milewsp1/file/'
APP_ADDRESS = "https://*SECRET*/"

USERS_FILES_PATH = "data/users/"
THUMBNAIL_PATH = "data/mini"
USER_FILES_LIMIT = 50
# To disallow XSS attacks - allowed extensions limitation
ALLOWED_EXTENSIONS_ENABLED = True
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

ENDPOINTS_RELATIVE_ADDRESSES = {
    "upload": APP_MAIN_ENDPOINT + "upload",
    "download": APP_MAIN_ENDPOINT + "download",
    "download_thumbnail": APP_MAIN_ENDPOINT + "download_thumbnail",
    "files": APP_MAIN_ENDPOINT + "files",
    "share": APP_MAIN_ENDPOINT + "share"
}

ENDPOINTS_FULL_ADDRESSES = {
    "upload": ENDPOINTS_RELATIVE_ADDRESSES["upload"],
    "download": ENDPOINTS_RELATIVE_ADDRESSES["download"],
    "download_thumbnail": ENDPOINTS_RELATIVE_ADDRESSES["download_thumbnail"],
    "files": ENDPOINTS_RELATIVE_ADDRESSES["files"],
    "share": ENDPOINTS_RELATIVE_ADDRESSES["share"]
}
