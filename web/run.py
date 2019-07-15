from flask import Flask, session, redirect
from flask import request

from record import r

from web.views.researcher import researcher
from web.views.community import community
from web.views.my_admin import my_admin
from web.views.login import login

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dogdong'
app.register_blueprint(researcher)
app.register_blueprint(community)
app.register_blueprint(my_admin)
app.register_blueprint(login)
# app.register_blueprint(user, url_prefix='/user')

app.config.update(SECRET_KEY=os.urandom(24))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.after_request
def record(response):
    lis = r.getCatalog()
    if lis[0] in r.map:
        method = r.map[lis[0]]
        method(lis, response)
    return response


# @app.before_request
# def is_login():
#     print("*"*20)
#     print(request.path)
#     if request.path == '/login' or request.path == '/login/logout':
#         return None
#     if not session.get('username'):
#         redirect('/login')


@app.context_processor
def my_context_processor():
    user = session.get('username')
    if user:
        return {'user_name': user}
    return {}


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", debug=True)
