from flask import Flask, render_template
from web.views.researcher import researcher
from web.views.community import community

app = Flask(__name__)
app.config['SECRET_KEY']='dogdong'
app.register_blueprint(researcher)
app.register_blueprint(community)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", debug=True)
