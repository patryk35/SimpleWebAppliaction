from flask import Flask, render_template, Response, redirect, url_for, flash, send_file
from flask import session
from flask import request
from config.configuration import SESSION_KEY, ENDPOINTS_ADDRESSES
from authorization import login
from functools import wraps
from authorization.login import check_user
from dashboard.dashboard import upload_file, get_file, get_user_files


app = Flask(__name__)
app.secret_key = SESSION_KEY
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

def authentication_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' in session and check_user(session['login'], session['password']):
            return func(*args, **kwargs)
        else:
            return Response("Access denied", "401 Unauthorized")

    return wrapper


@app.route('/milewsp1/app/login', methods=['POST', 'GET'])
def login_page():
    basics = {
        "login_endpoint": ENDPOINTS_ADDRESSES['login'],
        "not_found": False
    }
    if 'login' in session:
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        user_id = login.check_user(request.form["login"], request.form["password"])
        if user_id != "":
            session['login'] = request.form["login"]
            session['password'] = request.form["password"]
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        basics['not_found'] = True
        return render_template('login.html', basics=basics)
    return render_template('login.html', basics=basics)


@app.route('/milewsp1/app/upload', methods=['POST'])
@authentication_required
def upload():
    if 'file' not in request.files:
        flash('Aby dodać plik, muszisz go wybrać!')
        return redirect(url_for('dashboard'))
    file = request.files['file']

    if file.filename == '':
        flash('Aby dodać plik, muszisz go wybrać!')
        return redirect(url_for('dashboard'))
    res = ''
    try:
        file = request.files['file']
        message, res = upload_file(session['user_id'], file)
        flash(message)
    except AttributeError as e:
        flash("Spróbuj jeszcze raz!")
        redirect(url_for('dashboard'))

    if res:
        flash("_ok")
    return redirect(url_for('dashboard'))


@app.route('/milewsp1/app/download/<string:file_hash>', methods=['GET'])
@authentication_required
def download(file_hash):
    path, name = get_file(session['user_id'], file_hash)
    if name == 'not_found':
        return Response('Not found', '404 Not found')
    try:
        return send_file(path, attachment_filename=name, as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/milewsp1/app/dashboard', methods=['GET', 'POST'])
@authentication_required
def dashboard():
    basics = {
        "logout_endpoint": ENDPOINTS_ADDRESSES['logout'],
        "upload_endpoint": ENDPOINTS_ADDRESSES['upload'],
        "login": session['login']
    }
    files, links, length = get_user_files(session['user_id'], ENDPOINTS_ADDRESSES['download'] + "/")
    return render_template('dashboard.html', basics=basics, files=files, links=links, length=length)


@app.route('/milewsp1/app/logout')
@authentication_required
def logout():
    session.clear()
    return redirect(url_for('login_page'))


