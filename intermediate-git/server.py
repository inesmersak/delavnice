from bottle import redirect, request, response, route, run, template

import conf
import utils
from db import Database

DB = Database()
DB.connect()


@route('/')
def index():
    user_id = request.get_cookie('user', secret=conf.SECRET_KEY)
    user = None if user_id is None else DB.fetch_user_by_id(int(user_id))
    transactions = DB.fetch_user_transactions(user_id) if user_id is not None else None
    return template('index', user=user, transactions=transactions)


@route('/login')
def login():
    if request.get_cookie('user', secret=conf.SECRET_KEY) is not None:
        redirect('/')
    return template('login', error=False)


@route('/login', method='POST')
def login():
    if request.get_cookie('user', secret=conf.SECRET_KEY) is not None:
        redirect('/')
    user_id_tuple = DB.authenticate_user(**utils.get_forms_dict(request.forms))
    if user_id_tuple is not None:
        response.set_cookie('user', str(user_id_tuple[0]), secret=conf.SECRET_KEY)
        redirect('/')
    return template('login', error=True)


@route('/logout')
def logout():
    response.delete_cookie('user', secret=conf.SECRET_KEY)
    redirect('/')


@route('/register')
def register():
    if request.get_cookie('user', secret=conf.SECRET_KEY) is not None:
        redirect('/')
    return template('register', user_id=None, error=False)


@route('/register', method='POST')
def register():
    if request.get_cookie('user', secret=conf.SECRET_KEY) is not None:
        redirect('/')
    user_id = DB.add_user(**utils.get_forms_dict(request.forms))
    return template('register', user_id=user_id, error=True)


@route('/transfer')
def transfer():
    user_id = request.get_cookie('user', secret=conf.SECRET_KEY)
    user = None if user_id is None else DB.fetch_user_by_id(int(user_id))
    if user is None:
        redirect('/login')
    return template('transfer', current_user=user, users=DB.fetch_all_users())


@route('/transfer', method='POST')
def transfer():
    user_id = request.get_cookie('user', secret=conf.SECRET_KEY)
    if user_id is None:
        redirect('/login')
    user_id = int(user_id)
    success = DB.make_transaction(user_id, request.forms.get('to_user'), request.forms.get('value'))
    return template('transfer', success=success, current_user=DB.fetch_user_by_id(user_id), users=DB.fetch_all_users())


run(host='localhost', port=8080, reloader=True)
