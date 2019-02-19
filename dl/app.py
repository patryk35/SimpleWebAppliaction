import datetime
from functools import lru_cache, wraps

from flask import Flask, Response, send_file
from flask import request
from dl.dashboard.dashboard import upload_file, get_file, get_user_files, UPLOAD_STATUSES
from dl.config.configuration import APP_MAIN_ENDPOINT, ENDPOINTS_ADDRESSES, JWT_KEY
from dl.contract import PORT
from dl.p_jwt.jwt_decode import jwt_required

app = Flask(__name__)


@app.route(APP_MAIN_ENDPOINT + 'upload', methods=['POST'])
@jwt_required
def upload(user_id):
    if 'file' not in request.files:
        # flash('Aby dodać plik, muszisz go wybrać!')
        return Response('Missing file', '400 Not found')
    file = request.files['file']
    if file.filename == '':
        return Response('Missing file', '400 Not found')
    try:
        result = upload_file(user_id, file, file.filename)
        if result == UPLOAD_STATUSES['OK']:
            return Response('', '200 OK')
        elif result == UPLOAD_STATUSES['LIMIT_EXCEEDED']:
            return Response('', '409 Conflict')
        elif result == UPLOAD_STATUSES['WRONG_FILE_EXTENTION']:
            return Response('', '304 Not Modified')
        return Response('', '500 Internal Server Error')
        '''if res.status_code == 200:
            flash("Plik został dodany")
            flash("_ok")
        elif res.status_code == 304:
            flash("Możesz wgrać maksymalnie 5 plików")
        elif res.status_code == 409:
            flash("Nieprawidłowe rozszerzenie pliku. Możliwe: " + str(ALLOWED_FILES_EXTENSIONS))
        elif res.status_code == 500:
            flash("Upss.. coś poszło nie tak")'''
    except AttributeError:
        return Response('', '500 Internal server error')


@app.route(APP_MAIN_ENDPOINT + 'download/<string:file_hash>', methods=['GET'])
@jwt_required
def download(user_id, file_hash):
    path, name = get_file(user_id, file_hash)
    if name == 'not_found':
        return Response('Not found', '404 Not found')
    try:
        return send_file(path, attachment_filename=name, as_attachment=True)
    except BaseException:
        return Response('', '500 Internal Server Error')


@lru_cache(100)
@app.route(APP_MAIN_ENDPOINT + 'files', methods=['POST'])
@jwt_required
def files_list(user_id):
    print(user_id)
    download_endpoint_address = ENDPOINTS_ADDRESSES['download']
    res = get_user_files(user_id, download_endpoint_address)

    return Response(res, '200 OK')


if __name__ == "__main__":
    print(APP_MAIN_ENDPOINT + 'upload')
    app.run(port=PORT, debug=True)
