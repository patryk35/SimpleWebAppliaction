from functools import lru_cache
from flask import Flask, Response, send_file, abort
from flask import request
from dashboard.dashboard import upload_file, get_file, get_user_files, set_file_share_status, get_shared_file, \
    UPLOAD_STATUSES
from dashboard.dashboard import ERRORS as FILES_ERRORS
from config.configuration import ENDPOINTS_RELATIVE_ADDRESSES
from p_jwt.jwt_decode import jwt_required, jwt_required_header, decode_url_jwt

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['upload'], methods=['POST'])
@jwt_required
def upload(user_id):
    file = request.files['file']
    filename = request.form['file_name']
    try:
        result = upload_file(user_id, file, filename)
        if result == UPLOAD_STATUSES['OK']:
            return Response('OK', '200 OK')
        elif result == UPLOAD_STATUSES['LIMIT_EXCEEDED']:
            return Response('Limit exceeded', '409 Conflict')
        elif result == UPLOAD_STATUSES['WRONG_FILE_EXTENSION']:
            return Response('Wrong extension', '406 Not Acceptable')
        return Response('', '500 Internal Server Error')
    except AttributeError:
        return Response('', '500 Internal server error')


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['download'] + '/<string:file_hash>/<string:token>', methods=['GET'])
def download(file_hash, token):
    user_id = decode_url_jwt(token)
    path, name = get_file(user_id, file_hash)
    if name == 'not_found':
        return Response('Not found', '404 Not found')
    try:
        return send_file(path, attachment_filename=name, as_attachment=True)
    except BaseException:
        abort(500)


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['share'], methods=['PUT'])
@jwt_required
def share(user_id):
    switch = request.form['switch']
    file_hash = request.form['file_hash']
    if switch == "enable":
        result = set_file_share_status(user_id, file_hash, True)
    elif switch == "disable":
        result = set_file_share_status(user_id, file_hash, False)
    else:
        abort(405)

    if result == FILES_ERRORS['FILE_NOT_FOUND']:
        return Response('Not found', '404 Not found')
    return Response(result, '200 OK')


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['share'] + '/<string:hash>', methods=['GET'])
def share_access(file_hash):
    path, name = get_shared_file(file_hash)
    if name == FILES_ERRORS['FILE_NOT_FOUND']:
        return Response('Not Found', '404 Not Found')
    elif name == FILES_ERRORS['ACCESS_DENIED']:
        return Response('Unauthorized', '401 Unauthorized')
    try:
        return send_file(path, attachment_filename=name, as_attachment=True)
    except BaseException:
        abort(500)


@lru_cache(100)
@app.route(ENDPOINTS_RELATIVE_ADDRESSES['files'], methods=['POST'])
@jwt_required
def files_list(user_id):
    res = get_user_files(user_id)
    return Response(res, '200 OK')
