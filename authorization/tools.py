from hashlib import sha3_512,sha1

def hash_string(string):
    return sha3_512(string.encode()).hexdigest()

def hash_name(name):
    return sha1(name.encode()).hexdigest()




