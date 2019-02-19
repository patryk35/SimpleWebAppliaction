import datetime

from flask_jwt import jwt

from config.configuration import ENDPOINTS_FULL_ADDRESSES
from config.naming import FILE_ENDPOINTS_ADDRESSES, USER_FILES_LIMIT


def prepare_share_links(create_shared_links, share_links):
    n_share = [''] * USER_FILES_LIMIT
    n_share_access = [''] * USER_FILES_LIMIT
    for i in range(USER_FILES_LIMIT):
        if share_links[i] != '':
            # TODO: Create it like download with redirect
            n_share[i] = ENDPOINTS_FULL_ADDRESSES['share'] + "/" + create_shared_links[i] + "/disable"
            n_share_access[i] = ENDPOINTS_FULL_ADDRESSES['show_file_link'] + "/" + share_links[i]
        else:
            n_share[i] = ENDPOINTS_FULL_ADDRESSES['share'] + "/" + create_shared_links[i] + "/enable"
        i += 1
    return n_share, n_share_access



def prepare_download_links(links, has_thumbnail, token):
    n_links = [''] * USER_FILES_LIMIT
    n_min_links = [''] * USER_FILES_LIMIT
    i = 0
    for link in links:
        n_links[i] = FILE_ENDPOINTS_ADDRESSES['download'] + "/" + link + "/" + token.decode()
        if(has_thumbnail[i]):
            n_min_links[i] = FILE_ENDPOINTS_ADDRESSES['download_thumbnail'] + "/" + link + "/" + token.decode()
        else:
            n_min_links[i] = ""
        i += 1
    return n_links, n_min_links


def encode_auth_token(app, user_id, days=0, minutes=4):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, minutes=minutes),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('JWT_SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e
