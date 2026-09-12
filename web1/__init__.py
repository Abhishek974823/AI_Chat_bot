from flask import Flask

def create_app1():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hanadjnfdka'
    from .first import views
    app.register_blueprint(views,url_prefix='/')
    return app