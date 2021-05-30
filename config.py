import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-secret-key'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	    'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	POSTS_PER_PAGE = 3
	DEBUG=True
	TESTING=False
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_USERNAME = 'useitforuselessthings@gmail.com'
	MAIL_PASSWORD = 'Kumarswamy123'
	MAIL_PORT = 587
	MAIL_USE_TLS = True  
	MAIL_USE_SSL = False 
	MAIL_DEFAULT_SENDER = ('ganesh','useitforuselessthings@gmail.com') 
	MAIL_MAX_EMAILS = None
	MAIL_ASCII_ATTACHMENTS = None 
