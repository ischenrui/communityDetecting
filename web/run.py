from flask import Flask, render_template
from web.views.researcher import researcher
from web.views.my_admin import my_admin

app = Flask(__name__)

app.register_blueprint(researcher)
app.register_blueprint(my_admin)
# app.register_blueprint(user, url_prefix='/user')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", debug=True)
