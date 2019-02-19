import random

from config.configuration import USER_FILES_LIMIT, USERS_FILES_PATH, ALLOWED_EXTENSIONS, ALLOWED_EXTENSIONS_ENABLED
import os
import json
import datetime
import time
from werkzeug.utils import secure_filename
from hashlib import sha1

UPLOAD_STATUSES = {
    "OK": 100,
    "LIMIT_EXCEEDED": 200,
    "WRONG_FILE_EXTENSION": 300
}

ERRORS = {
    "FILE_NOT_FOUND": -100,
    "ACCESS_DENIED": -200
}


def hash_name(name):
    return sha1(name.encode()).hexdigest()


def upload_file(user_id, file, filename):
    # Checking if user has not more than USER_FILES_LIMIT files.
    # Whether user doesn't have folder yet - create it and json info file.
    directory = hash_name(str(user_id))
    origin_path = USERS_FILES_PATH + directory
    path = os.path.join(origin_path, "files.json")

    if not os.path.exists(origin_path):
        os.mkdir(origin_path)
        with open(path, "w") as wfile:
            wfile.write("{\n\"count\":0,\n\"content\": [\n]\n}")
            wfile.close()
    elif check_files_limit(origin_path) >= USER_FILES_LIMIT:
        return UPLOAD_STATUSES['LIMIT_EXCEEDED']

    if file and allowed_file(filename):
        filename = secure_filename(filename)
        timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        file_hash = hash_name(filename + str(user_id) + str(timestamp))
        file.save(os.path.join(origin_path, file_hash))
        update_json_file(origin_path, filename, file_hash, timestamp)
        return UPLOAD_STATUSES['OK']
    else:
        return UPLOAD_STATUSES['WRONG_FILE_EXTENSION']


def check_files_limit(directory):
    path = os.path.join(directory, "files.json")
    with open(path, "r") as file:
        files = json.load(file)
        file.close()
        return files['count']


def allowed_file(filename):
    if not ALLOWED_EXTENSIONS_ENABLED:
        return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def update_json_file(directory, filename, file_hash, timestamp):
    file_object = {
        "origin_name": filename,
        "hash": file_hash,
        "timestamp": timestamp,
        "is_shared": False,
        "share_stamp": ""
    }
    path = os.path.join(directory, "files.json")
    with open(path, "r") as file:
        files = json.load(file)
        file.close()
    files['content'].append(file_object)
    files['count'] = files['count'] + 1
    with open(path, "w") as file:
        json.dump(files, file)
        file.close()


def get_file(user_id, file_hash):
    directory = hash_name(str(user_id))
    path = USERS_FILES_PATH + directory  # + "/" + file_hash
    json_path = USERS_FILES_PATH + directory + "/files.json"
    name = "not_found"
    with open(json_path, "r") as file:
        files = json.load(file)
        file.close()
        for f in files['content']:
            if f['hash'] == file_hash:
                name = f['origin_name']
                break
    path += "/" + file_hash
    return path, name


def get_file(user_id, file_hash):
    directory = hash_name(str(user_id))
    path = USERS_FILES_PATH + directory  # + "/" + file_hash
    json_path = USERS_FILES_PATH + directory + "/files.json"
    name = "not_found"
    with open(json_path, "r") as file:
        files = json.load(file)
        file.close()
        for f in files['content']:
            if f['hash'] == file_hash:
                name = f['origin_name']
                break
    path += "/" + file_hash
    return path, name


def get_user_files(user_id):
    user_files = [''] * 5
    files_address = [''] * 5
    share_links = [''] * 5
    length = 0
    directory = hash_name(str(user_id))
    json_path = USERS_FILES_PATH + directory + "/files.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            files = json.load(file)
            file.close()
            for f in files['content']:
                if len(f['origin_name']) > 15:
                    name = f['origin_name'][:15] + "..." + f['origin_name'][-5:]
                else:
                    name = f['origin_name']
                user_files[length] = name
                files_address[length] = f['hash']
                if f['share_stamp'] != '':
                    share_links[length] = directory + f['hash'] + f['share_stamp']
                length += 1
    res = {}
    res['user_files'] = user_files
    res['files_address'] = files_address
    res['share_links'] = share_links
    res['length'] = length
    return json.dumps(res)


def set_file_share_status(user_id, file_hash, switch):
    # Randomize share_links by adding to link timestamp and random string
    directory = hash_name(str(user_id))
    if switch:
        timestamp = int(round(time.time() * 1000))
        share_stamp = hash_name(str(random.randint(0, timestamp)))
        share_hash = directory + file_hash + share_stamp
    else:
        share_stamp = ""
        share_hash = ""

    # Set file flag as shared and add share_hash to file data
    json_path = USERS_FILES_PATH + directory + "/files.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            files = json.load(file)
            file.close()
            found = False
            for f in files['content']:
                if f['hash'] == file_hash:
                    f['is_shared'] = switch
                    f['share_stamp'] = share_stamp
                    found = True
                    break
            if not found:
                return ERRORS['FILE_NOT_FOUND']
    with open(json_path, "w") as file:
        json.dump(files, file)
        file.close()
    return share_hash


def get_shared_file(hash):
    # TODO: Move it to some function
    share_stamp = hash[80:]
    directory = hash[0:40]
    file_hash = hash[40:80]
    path = USERS_FILES_PATH + directory  # + "/" + file_hash
    json_path = USERS_FILES_PATH + directory + "/files.json"
    name = ERRORS['FILE_NOT_FOUND']
    with open(json_path, "r") as file:
        files = json.load(file)
        file.close()
        for f in files['content']:
            if f['hash'] == file_hash and f['is_shared'] == True and f['share_stamp'] == share_stamp:
                name = f['origin_name']
                break
            elif f['hash'] == file_hash:
                return path, ERRORS['ACCESS_DENIED']
    path += "/" + file_hash
    return path, name

