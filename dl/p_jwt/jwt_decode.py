from functools import wraps

from flask import request, Response, abort
from flask_jwt import jwt

from config.configuration import JWT_KEY

JWT_TOKEN_EXPIRED = -100
JWT_INVALID_TOKEN = -200


def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.form['authorization']
        user_id = decode_auth_token(token.encode())
        if int(user_id) > 0:
            return func(user_id, *args, **kwargs)
        elif user_id == JWT_INVALID_TOKEN:
            return Response(response=None, status='401 Unauthorized')
        elif user_id == JWT_TOKEN_EXPIRED:
            return Response(response=None, status='408 Request Timeout')
        return Response(response=None, status='500 Internal Server Error')

    return wrapper


def jwt_required_header(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
            user_id = decode_auth_token(token.encode())
            try:
                user_id = int(user_id)
            except BaseException:
                abort(401)
            if user_id != "":
                return func(user_id, *args, **kwargs)
            return Response(response=None, status='500 Internal Server Error')
        abort(401)

    return wrapper

def decode_url_jwt(token):
    user_id = decode_auth_token(token)
    try:
        user_id = int(user_id)
    except BaseException:
        abort(401)
    if user_id != "":
        return user_id
    abort(401)


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, JWT_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return JWT_TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return JWT_INVALID_TOKEN
