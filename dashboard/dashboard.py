from config.configuration import USER_FILES_LIMIT, USERS_FILES_PATH, ALLOWED_EXTENSIONS, ALLOWED_EXTENSIONS_ENABLED
from authorization.tools import hash_name
import os
import json
import datetime
from werkzeug.utils import secure_filename


def upload_file(user_id, file):
    # Checking if user has not more than USER_FILES_LIMIT files.
    # Whether user doesn't have folder yet - create it and json info file.
    directory = hash_name(str(user_id))
    origin_path = USERS_FILES_PATH + directory
    path = os.path.join(origin_path, "files.json")
    res = False
    if not os.path.exists(origin_path):
        os.mkdir(origin_path)
        with open(path, "w") as wfile:
            wfile.write("{\n\"count\":0,\n\"content\": [\n]\n}")
            wfile.close()
    elif check_files_limit(origin_path) >= USER_FILES_LIMIT:
        return "Możesz wgrać maksymalnie 5 plików", res

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        file_hash = hash_name(filename + str(user_id) + str(timestamp))
        file.save(os.path.join(origin_path, file_hash))
        update_json_file(origin_path, filename, file_hash, timestamp)
        res = True
        return "Plik został dodany", res
    else:
        return "Nieprawidłowe rozszerzenie pliku. Możliwe: " + str(ALLOWED_EXTENSIONS), res


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
        "timestamp": timestamp
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


def get_user_files(user_id, download_endpoint_address):
    user_files = [''] * 5
    files_address = [''] * 5
    length = 0
    directory = hash_name(str(user_id))
    json_path = USERS_FILES_PATH + directory + "/files.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as file:
            files = json.load(file)
            file.close()
            for f in files['content']:
                if len(f['origin_name']) > 25:
                    name = f['origin_name'][:25] + "..." + f['origin_name'][-5:]
                else:
                    name = f['origin_name']
                user_files[length] = name
                files_address[length] = (download_endpoint_address + f['hash'])
                length += 1
    return user_files, files_address, length

