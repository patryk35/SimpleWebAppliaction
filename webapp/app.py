import datetime
import uuid

import requests
import redis
from flask import Flask, render_template, redirect, url_for, flash, Response, jsonify
from flask import session
from flask import request
from functools import wraps, lru_cache
from config.configuration import ENDPOINTS_RELATIVE_ADDRESSES, ENDPOINTS_FULL_ADDRESSES, SSL_CERTIFICATE_VERIFY, \
    LAYOUT_PARAMETERS, LONG_POLLING_JS_FILE
from config.naming import FILE_ENDPOINTS_ADDRESSES
from dashboard.tools import prepare_download_links, encode_auth_token, prepare_share_links
from dashboard.UploadedFile import UploadedFile
from config import constants
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException


# TODO(High): Czyszczenie css, poprawa struktury na serwerze, dodanie samodzielnych scss, doadnie tego do main folderu
# TODO(High): Sprawko: 3x screeny x3 + performance tests - usunac czcionki???
# TODO(Medium): Review endpoints and check if it is correct with REST or rewrite it flask restful
# TODO(Medium): Create repo for project
# TODO(Low): Create function create_link to add "/" for link elems when it is necessary and then remove ".../"
#  from naming and dl config
# TODO(Low): Do cleaning in messages - flash. The best way is creating function to operate on flash
# TODO(Minor): Funny error site
# TODO(Minor): Deployment script
# TODO(Minor): Debug and Production configurations
''' def flash_function(isCorrect, *args):

    '''

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'

app = Flask(__name__)
app.secret_key = env.get(constants.SECRET_KEY)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['JWT_SECRET_KEY'] = env.get(constants.JWT_SECRET_KEY)

red = redis.StrictRedis(host='localhost', port=6379, db=0)

recently_uploaded_files = {}


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


'''Authorization section'''

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


def authentication_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect(url_for('authorization_page'))
        return func(*args, **kwargs)

    return decorated


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['callback'])
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    session_key = uuid.uuid1()
    session['session_key'] = str(session_key)
    red.set(str(session_key), userinfo['sub'])
    return redirect(url_for('dashboard'))


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['login_auth'], methods=['GET'])
def login_auth():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['logout'])
@authentication_required
def logout():
    session.clear()
    params = {'returnTo': url_for('authorization_page', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@lru_cache(100)
def get_user_by_session_key(session_key):
    user_id = red.get(session_key)
    if user_id != "":
        return user_id
    return ""


''' Sites section'''


def app_site_wrapper(template, parameters):
    user_parameters = {
        'logged_in': 0
    }

    parameters['current_site'] = template.split(".")[0]
    print(parameters['current_site'])
    if constants.PROFILE_KEY in session:
        user_parameters['login'] = session[constants.PROFILE_KEY]['name']
        user_parameters['logged_in'] = 1
    return render_template(template, parameters=parameters, user_parameters=user_parameters,
                           layout_parameters=LAYOUT_PARAMETERS)


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['authorization'], methods=['GET'])
def authorization_page():
    parameters = {
        "login_auth_endpoint": ENDPOINTS_FULL_ADDRESSES['login_auth'],
        "logout_auth_endpoint": ENDPOINTS_FULL_ADDRESSES['logout']
    }
    return app_site_wrapper('authorization.html', parameters=parameters)


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['upload_site'], methods=['GET', 'POST'])
@authentication_required
def upload_site():
    token = encode_auth_token(app, get_user_by_session_key(session['session_key']).decode())
    parameters = {
        "upload_endpoint": ENDPOINTS_FULL_ADDRESSES['upload_endpoint'],
        "logout_endpoint": ENDPOINTS_FULL_ADDRESSES['logout'],
        "token": token
    }
    return app_site_wrapper('upload.html', parameters)


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['dashboard'], methods=['GET', 'POST'])
@authentication_required
def dashboard():
    parameters = {
        "logout_endpoint": ENDPOINTS_FULL_ADDRESSES['logout'],
        "files": [],
        "download_links": [],
        "length": 0,
        "share_links": [],
        "show_links": [],
        "long_polling_js": LONG_POLLING_JS_FILE
    }
    try:
        token = encode_auth_token(app, get_user_by_session_key(session['session_key']).decode())
        data = {'authorization': token}
        res = requests.post(FILE_ENDPOINTS_ADDRESSES['files'], data=data, verify=SSL_CERTIFICATE_VERIFY)
        files_info = res.json()
        parameters['files'] = files_info['user_files']
        parameters['download_links'] = prepare_download_links(files_info['files_address'], token)
        parameters['share_links'], parameters['show_links'] = prepare_share_links(files_info['files_address'],
                                                                                  files_info['share_links'])
        parameters['length'] = files_info['length']
    except BaseException:
        flash(
            "Problem z połączeniem. Lista plików jest nieosiągalna. "
            "Spróbuj za chwilę ...")
    return app_site_wrapper('dashboard.html', parameters)


'''Endpoints section'''


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['upload_endpoint'], methods=['POST'])
@authentication_required
def upload():
    if 'file' not in request.files:
        flash('Aby dodać plik, muszisz go wybrać!')
        return redirect(url_for('upload_site'))
    file = request.files['file']

    if file.filename == '':
        flash('Aby dodać plik, musisz go wybrać!')
        return redirect(url_for('upload_site'))
    try:
        token = request.form['authorization']
        token_str = token[2:-1]
        data = {'authorization': token_str,
                'file_name': file.filename}
        result = requests.post(FILE_ENDPOINTS_ADDRESSES['upload'], data=data, files=request.files,
                               verify=SSL_CERTIFICATE_VERIFY)
        if result.status_code == 200:
            flash("Pomyślnie dodano!")
            flash("_valid")
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(seconds=2)
            recently_uploaded_files[session[constants.PROFILE_KEY]['name']] = UploadedFile(file.filename, expire_date,
                                                                                           session['session_key'])
        elif result.status_code == 406:
            flash("Nieprawidłowe rozszerzenie pliku. Dozwolone: 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'")
        elif result.status_code == 409:
            flash("Limit osiągniety. Nie możesz dodać więcej niż 5 plików.")
        else:
            flash("Wystąpił problem podczas dodawania pliku!")
    except AttributeError:
        flash("Spróbuj jeszcze raz!")
        return redirect(url_for('upload_site'))

    return redirect(url_for('upload_site'))


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['share'] + '/<string:file_hash>/<string:switch>', methods=['GET'])
@authentication_required
def share(file_hash, switch):
    try:
        token = encode_auth_token(app, get_user_by_session_key(session['session_key']).decode())
        data = {'authorization': token,
                'file_hash': file_hash,
                'switch': switch}
        result = requests.put(FILE_ENDPOINTS_ADDRESSES['share'], data=data, verify=SSL_CERTIFICATE_VERIFY)
        if result.status_code == 200:
            if result.text != "":
                flash("Pomyślnie udostępniono plik!")
                flash("_valid")
                flash(FILE_ENDPOINTS_ADDRESSES['share'] + "/" + result.text)
            else:
                flash("Pomyślnie anulowano udostępnianie pliku!")
                flash("_valid")
        elif result.status_code == 404:
            flash("Nie znaleziono pliku")
        else:
            flash("Wystąpił problem podczas zmainy statusu udostępnienia pliku!")
    except AttributeError:
        flash("Spróbuj jeszcze raz!")
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['show_file_link'] + '/<string:hash>', methods=['GET'])
@authentication_required
def show_link(hash):
    flash("Link do Twojego pliku:")
    flash("_valid")
    flash(FILE_ENDPOINTS_ADDRESSES['share'] + "/" + hash)
    return redirect(url_for('dashboard'))


# 2 methods below are used for long-polling communicates about uploading files
@authentication_required
@app.route(ENDPOINTS_RELATIVE_ADDRESSES['long_polling_notify'], methods=['POST'])
def long_polling_notify():
    uploaded_file = False
    if session[constants.PROFILE_KEY]['name'] in recently_uploaded_files.keys():
        file = recently_uploaded_files[session[constants.PROFILE_KEY]['name']]
        if file.is_valid():
            uploaded_file = True
        else:
            recently_uploaded_files.pop(session[constants.PROFILE_KEY]['name'])
    if uploaded_file:
        return Response('newFile', status=200)
    return Response('none', status=200)


@authentication_required
@app.route(ENDPOINTS_RELATIVE_ADDRESSES['polling_data'], methods=['GET'])
def polling_data():
    file = recently_uploaded_files[session[constants.PROFILE_KEY]['name']]
    if file and not file.communicate_showed_in_session(session['session_key']):
        file.add_session_to_showed(session['session_key'])
        return Response("Dodano nowy plik. Odśwież stronę by go zobaczyć.", status=200)
    return Response(status=200)
