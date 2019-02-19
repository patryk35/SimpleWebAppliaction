import datetime
import json

import requests
from flask import Flask, render_template, Response, redirect, url_for, flash, send_file
from flask import session
from flask import request
from functools import wraps
from webapp.config.configuration import SESSION_KEY, ENDPOINTS_ADDRESSES, APP_MAIN_ENDPOINT, JWT_KEY
from webapp.authorization.login import check_user
from dl.contract import ALLOWED_FILES_EXTENSIONS
from flask_jwt import jwt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

app = Flask(__name__)
app.secret_key = SESSION_KEY
#app.config['SESSION_COOKIE_SECURE'] = True # TODO: Set it back
app.config['SESSION_COOKIE_HTTPONLY'] = True

app.config['JWT_SECRET_KEY'] = JWT_KEY
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=1000)


def authentication_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' in session and check_user(session['login'], session['password']):
            return func(*args, **kwargs)
        else:
            return Response("Access denied", "401 Unauthorized")

    return wrapper


@app.route(APP_MAIN_ENDPOINT + 'login', methods=['POST', 'GET'])
def login_page():
    basics = {
        "login_endpoint": ENDPOINTS_ADDRESSES['login'],
        "not_found": False
    }
    if 'login' in session:
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        user_id = check_user(request.form["login"], request.form["password"])
        if user_id != "":
            session['login'] = request.form["login"]
            session['password'] = request.form["password"]
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        basics['not_found'] = True
        return render_template('login.html', basics=basics)
    return render_template('login.html', basics=basics)


@app.route(APP_MAIN_ENDPOINT + 'upload', methods=['POST'])
@authentication_required
def upload():
    '''uri = 'http://localhost:5001/upload'
    if 'file' not in request.files:
        flash('Aby dodać plik, muszisz go wybrać!')
        return redirect(url_for('dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('Aby dodać plik, muszisz go wybrać!')
        return redirect(url_for('dashboard'))
    try:
        values = {'upload_file': file.filename}
        res = requests.post(uri, files=request.files, data=values)
        if res.status_code == 200:
            flash("Plik został dodany")
            flash("_ok")
        elif res.status_code == 304:
            flash("Możesz wgrać maksymalnie 5 plików")
        elif res.status_code == 409:
            flash("Nieprawidłowe rozszerzenie pliku. Możliwe: " + str(ALLOWED_FILES_EXTENSIONS))
        elif res.status_code == 500:
            flash("Upss.. coś poszło nie tak")
    except AttributeError:
        flash("Spróbuj jeszcze raz!")'''
    return redirect(url_for('dashboard'))

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=100),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('JWT_SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


@app.route(APP_MAIN_ENDPOINT + 'dashboard', methods=['GET', 'POST'])
@authentication_required
def dashboard():
    basics = {
        "logout_endpoint": ENDPOINTS_ADDRESSES['logout'],
        "login": session['login']
    }
    #token = create_access_token(identity=session['user_id'])
    token = encode_auth_token(session['user_id']).decode()
    print(token)
    try:
        uri = 'http://localhost:5001/files'
        data = {'authorization':token}
        res = requests.post(uri, data=data)
        files_info = res.json()
        files = files_info['user_files']
        links = files_info['files_address']
        length = files_info['length']
        return render_template('dashboard.html', basics=basics, files=files, links=links, length=length, token=token)
    except BaseException:
        flash("Problem z połączeniem - lista plików nie została zaktualizowana, spróbuj za chwilę ...")
        return render_template('dashboard.html', basics=basics, files=[], links=[], length=0, token=token)

@app.route(APP_MAIN_ENDPOINT + 'logout')
@authentication_required
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# TODO(high): Session key in cookies and no id
# TODO(medium): Write it in flaskrestful
# TODO(high): What if api doesnt works
# TODO(high): js -> get_token(), if is expired - refresh it

if __name__ == "__main__":
    app.run(port=5000, debug=True)


