import json
import uuid

from authorization.tools import hash_string
from functools import lru_cache
import redis


@lru_cache(100)
def check_user(user, password):
    # not effective but users file has just a few records
    if user is None or password is None:
        return ""
    with open('config/users.json', "r") as users:
        records = json.load(users)
        users.close()
        for usr in records['users']:
            if usr['login'] == user and usr['password'] == hash_string(password):
                session_key = uuid.uuid1()
                r = redis.StrictRedis(host='localhost', port=6379, db=0)
                r.set(str(session_key), usr['id'])
                return str(session_key)
    return ""


@lru_cache(100)
def get_user_by_session_key(session_key):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    user_id = r.get(session_key)
    if user_id != "":
        return user_id
    return ""


def update_json_file(users):
    with open('config/users.json', "w") as file:
        json.dump(users, file)
        file.close()


def dispose_user_session(session_key):
    with open('config/users.json', "r") as users:
        users.close()
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.delete(session_key)
    return False
