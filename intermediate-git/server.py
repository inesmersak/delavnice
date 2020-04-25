from bottle import request, route, run, template
from db import Database

DB = Database()
DB.connect()

@route('/')
def index():
    return template('index')


@route('/register')
def register():
    return template('register', user_id=None, error=False)


@route('/register', method='POST')
def register():
    user_id = DB.add_user(**dict(request.forms))
    return template('register', user_id=user_id, error=True)


run(host='localhost', port=8080, reloader=True)
