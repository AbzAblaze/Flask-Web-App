from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#Database
db = SQLAlchemy()
USER_DB_NAME = "users.db"
TEST_DB_NAME = 'chinook.db'

#Create App
def create_app():
    #Configs
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ajkldjdifoi2'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{USER_DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'two' : f'sqlite:///{TEST_DB_NAME}'}
    db.init_app(app)

    #Import Blueprints
    from .views import views
    from .auth  import auth
    #Import Models
    from .models import User
    #Create the Database Tables
    with app.app_context():
        db.create_all()
    #Register Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  #Where to go if not logged in
    login_manager.init_app(app)
    #Load User Data from User db
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    #Return
    return app
