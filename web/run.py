from flask import Flask, render_template

from record import r

from web.views.researcher import researcher
from web.views.community import community
from web.views.my_admin import my_admin
from web.views.login import login

import os

app = Flask(__name__)
app.config['SECRET_KEY']='dogdong'
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


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", debug=True)
