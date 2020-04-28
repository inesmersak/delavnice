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
    return template('index', user=user)


@route('/login')
def login():
    return template('login', register=False, error=False)


@route('/login', method='POST')
def login():
    user_id_tuple = DB.authenticate_user(**utils.get_forms_dict(request.forms))
    if user_id_tuple is not None:
        response.set_cookie('user', str(user_id_tuple[0]), secret=conf.SECRET_KEY)
        redirect('/')
    return template('login', register=False, error=True)


@route('/logout')
def logout():
    response.delete_cookie('user', secret=conf.SECRET_KEY)
    redirect('/')


@route('/register')
def register():
    return template('register', user_id=None, error=False)


@route('/register', method='POST')
def register():
    user_id = DB.add_user(**utils.get_forms_dict(request.forms))
    return template('register', user_id=user_id, error=True)


run(host='localhost', port=8080, reloader=True)
