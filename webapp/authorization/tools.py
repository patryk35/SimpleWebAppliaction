from hashlib import sha3_512


def hash_string(string):
    return sha3_512(string.encode()).hexdigest()
