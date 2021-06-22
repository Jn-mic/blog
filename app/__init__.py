from flask import Flask
import flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
bootstrap = Bootstrap(app)
mail = Mail(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'
login_manager.login_message_category = 'info'



def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])


    #initialize extensions
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    
    # configure UploadSet
    
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    return app
