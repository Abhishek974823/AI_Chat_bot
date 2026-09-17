from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def create_app1():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hanadjnfdka'
    from .first import views
    app.register_blueprint(views,url_prefix='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
    db.init_app(app)
    return app