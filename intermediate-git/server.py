from bottle import route, run, template


@route('/')
def index():
    return template('index')


run(host='localhost', port=8080, reloader=True)