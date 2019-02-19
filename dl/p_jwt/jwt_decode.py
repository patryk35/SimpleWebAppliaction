from functools import wraps

from flask import request, Response
from flask_jwt import jwt

from dl.config.configuration import JWT_KEY

JWT_TOKEN_EXPIRED = -100
JWT_INVALID_TOKEN = -200


def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.form['authorization']
        user_id = decode_auth_token(token.encode())
        if user_id > 0:
            return func(user_id, *args, **kwargs)
        elif user_id == JWT_INVALID_TOKEN:
            return Response(response=None, status='401 Unauthorized')
        elif user_id == JWT_TOKEN_EXPIRED:
            return Response(response=None, status='408 Request Timeout')
        return Response(response=None, status='500 Internal Server Error')

    return wrapper


def decode_auth_token(auth_token):
    try:
        print(auth_token.decode())
        payload = jwt.decode(auth_token, JWT_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return JWT_TOKEN_EXPIRED
    except jwt.InvalidTokenError:
        return JWT_INVALID_TOKEN
