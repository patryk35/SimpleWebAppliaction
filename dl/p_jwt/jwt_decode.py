from functools import wraps

from flask import request, Response, abort
from flask_jwt import jwt

JWT_TOKEN_EXPIRED = -100
JWT_INVALID_TOKEN = -200


def jwt_required(jwt_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.form['authorization']
            user_id = decode_auth_token(token.encode(), jwt_key)
            if user_id[0:5] == "auth0":
                return func(user_id, *args, **kwargs)
            elif user_id == JWT_INVALID_TOKEN:
                return Response(response=None, status='401 Unauthorized')
            elif user_id == JWT_TOKEN_EXPIRED:
                return Response(response=None, status='408 Request Timeout')
            return Response(response=None, status='500 Internal Server Error')
        return wrapper
    return decorator


def jwt_required_header(jwt_key):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' in request.headers:
                token = request.headers.get('Authorization')
                user_id = decode_auth_token(token.encode(), jwt_key)
                try:
                    user_id = int(user_id)
                except BaseException:
                    abort(401)
                if user_id != "":
                    return func(user_id, *args, **kwargs)
                return Response(response=None, status='500 Internal Server Error')
            abort(401)
        return wrapper
    return decorator


def decode_url_jwt(token, jwt_key):
    print(token)
    print(jwt_key)
    user_id = decode_auth_token(token, jwt_key)
    if user_id[0:5] == "auth0":
        return user_id
    abort(401)


def decode_auth_token(auth_token, jwt_key):
    try:
        payload = jwt.decode(auth_token, jwt_key)

        return payload['sub']
    except jwt.ExpiredSignatureError:
        return JWT_TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return JWT_INVALID_TOKEN
