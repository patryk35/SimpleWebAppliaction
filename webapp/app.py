import datetime
import requests
from flask import Flask, render_template, redirect, url_for, flash, Response
from flask import session
from flask import request
from functools import wraps
from config.configuration import SESSION_KEY, ENDPOINTS_RELATIVE_ADDRESSES, JWT_KEY, ENDPOINTS_FULL_ADDRESSES, \
    SSL_CERTIFICATE_VERIFY
from config.naming import FILE_ENDPOINTS_ADDRESSES
from authorization.login import check_user, get_user_by_session_key, dispose_user_session
from dashboard.tools import prepare_download_links, encode_auth_token, prepare_share_links
from dashboard.UploadedFile import UploadedFile

app = Flask(__name__)
app.secret_key = SESSION_KEY
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

app.config['JWT_SECRET_KEY'] = JWT_KEY

recently_uploaded_files = {}


def authentication_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'session_key' in session and session['session_key'] != "" and get_user_by_session_key(
                session['session_key']):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login_page'))

    return wrapper


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['login'], methods=['POST', 'GET'])
def login_page():
    basics = {
        "login_endpoint": ENDPOINTS_FULL_ADDRESSES['login'],
        "not_found": False
    }
    if 'login' in session:
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        session_key = check_user(request.form["login"], request.form["password"])
        if session_key != "":
            session['session_key'] = session_key
            session['login'] = request.form['login']
            return redirect(url_for('dashboard'))
        basics['not_found'] = True
        return render_template('login.html', basics=basics)
    return render_template('login.html', basics=basics)


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['dashboard'], methods=['GET', 'POST'])
@authentication_required
def dashboard():
    basics = {
        "logout_endpoint": ENDPOINTS_FULL_ADDRESSES['logout'],
        "login": session['login']
    }
    token = encode_auth_token(app, get_user_by_session_key(session['session_key']).decode())
    try:
        token = encode_auth_token(app, get_user_by_session_key(session['session_key']).decode())
        data = {'authorization': token}
        res = requests.post(FILE_ENDPOINTS_ADDRESSES['files'], data=data, verify=SSL_CERTIFICATE_VERIFY)
        files_info = res.json()
        files = files_info['user_files']
        download_links = prepare_download_links(files_info['files_address'], token)
        share_links, show_links = prepare_share_links(files_info['files_address'], files_info['share_links'])
        length = files_info['length']
        return render_template('dashboard.html', basics=basics, files=files, download_links=download_links,
                               length=length, token=token, share_links=share_links,
                               show_links=show_links )
    except BaseException as e:
        flash("Problem z połączeniem - lista plików nie została zaktualizowana, spróbuj za chwilę ...")
        return render_template('dashboard.html', basics=basics, files=[], download_links=[], length=0, token=token,
                               share_links=[], show_links=[])


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['upload'], methods=['POST'])
@authentication_required
def upload():
    if 'file' not in request.files:
        flash('Aby dodać plik, muszisz go wybrać!')
        return redirect(url_for('dashboard'))
    file = request.files['file']

    if file.filename == '':
        flash('Aby dodać plik, musisz go wybrać!')
        return redirect(url_for('dashboard'))
    try:
        token = request.form['authorization']
        token_str = token[2:-1]
        data = {'authorization': token_str,
                'file_name': file.filename}
        result = requests.post(FILE_ENDPOINTS_ADDRESSES['upload'], data=data, files=request.files,
                               verify=SSL_CERTIFICATE_VERIFY)
        if result.status_code == 200:
            flash("Pomyślnie dodano!")
            flash("_ok")
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(seconds=2)
            recently_uploaded_files[session['login']] = UploadedFile(file.filename, expire_date, session['session_key'])
        elif result.status_code == 406:
            flash("Nieprawidłowe rozszerzenie pliku. Dozwolone: 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'")
        elif result.status_code == 409:
            flash("Limit osiągniety. Nie możesz dodać więcej niż 5 plików.")
        else:
            flash("Wystąpił problem podczas dodawania pliku!")
    except AttributeError:
        flash("Spróbuj jeszcze raz!")
        return redirect(url_for('dashboard'))

    return redirect(url_for('dashboard'))


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['share'] + '/<string:hash>/<string:switch>', methods=['GET'])
@authentication_required
def share(hash, switch):
    try:
        token = encode_auth_token(app, get_user_by_session_key(session['session_key']).decode())
        data = {'authorization': token,
                'file_hash': hash,
                'switch': switch}
        result = requests.put(FILE_ENDPOINTS_ADDRESSES['share'], data=data, verify=SSL_CERTIFICATE_VERIFY)
        if result.status_code == 200:
            if result.text != "":
                flash("Pomyślnie udostępniono plik!")
                flash("_ok")
                flash(FILE_ENDPOINTS_ADDRESSES['share'] + "/" + result.text)
            else:
                flash("Pomyślnie anulowano udostępnianie pliku!")
                flash("_ok")
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
    flash("_ok")
    flash(FILE_ENDPOINTS_ADDRESSES['share'] + "/" + hash)
    return redirect(url_for('dashboard'))


@app.route(ENDPOINTS_RELATIVE_ADDRESSES['logout'])
@authentication_required
def logout():
    dispose_user_session(session['session_key'])
    session.clear()
    return redirect(url_for('login_page'))


# 2 methods below are used for long-polling communicates about uploading files
@authentication_required
@app.route(ENDPOINTS_RELATIVE_ADDRESSES['long_polling_notify'], methods=['POST'])
def long_polling_notify():
    uploaded_file = False
    if session['login'] in recently_uploaded_files.keys():
        file = recently_uploaded_files[session['login']]
        if file.is_valid():
            uploaded_file = True
        else:
            recently_uploaded_files.pop(session['login'])
    if uploaded_file:
        return Response('newFile', status=200)
    return Response('none', status=200)


@authentication_required
@app.route(ENDPOINTS_RELATIVE_ADDRESSES['polling_data'], methods=['GET'])
def polling_data():
    file = recently_uploaded_files[session['login']]
    if file and not file.communicate_showed_in_session(session['session_key']):
        file.add_session_to_showed(session['session_key'])
        return Response("Dodano nowy plik. Odśwież stronę by go zobaczyć.", status=200)
    return Response(status=200)
