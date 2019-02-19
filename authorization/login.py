import json
from authorization.tools import hash_string
from functools import lru_cache


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
                return usr['id']
    return ""
