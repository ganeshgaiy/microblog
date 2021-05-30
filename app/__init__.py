from flask import Flask
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask('app')    #1) 
app.config.from_object(Config)  #3)
db = SQLAlchemy(app)
migrate = Migrate(app,db) #2) 
mail = Mail(app)
bootstrap = Bootstrap(app)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'
moment = Moment(app)

from app import routes,models


#1) https://stackoverflow.com/questions/39393926/flaskapplication-versus-flask-name#:~:text=__name__%20is%20just,files%2C%20instance%20folder%2C%20etc.

#2) should be app,db. you will get an error if you interchange[error:Key error migrate]

"""
#3)
class Config(dict):
    Works exactly like a dict but provides ways to fill it from files
    or special dictionaries.  There are two common patterns to populate the
    config.

    Either you can fill the config from a config file::

        app.config.from_pyfile('yourconfig.cfg')

    Or alternatively you can define the configuration options in the
    module that calls :meth:`from_object` or provide an import path to
    a module that should be loaded.  It is also possible to tell it to
    use the same module and with that provide the configuration values
    just before the call::

        DEBUG = True
        SECRET_KEY = 'development key'
        app.config.from_object(__name__)

    In both cases (loading from any Python file or loading from modules),
    only uppercase keys are added to the config.  This makes it possible to use
    lowercase values in the config file for temporary values that are not added
    to the config or to define the config keys in the same file that implements
    the application.

    Probably the most interesting way to load configurations is from an
    environment variable pointing to a file::

        app.config.from_envvar('YOURAPPLICATION_SETTINGS')

    In this case before launching the application you have to set this
    environment variable to the file you want to use.  On Linux and OS X
    use the export statement::

        export YOURAPPLICATION_SETTINGS='/path/to/config/file'

    On windows use `set` instead."""

