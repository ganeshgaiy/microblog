from app import db,login
from werkzeug.security import generate_password_hash,check_password_hash
from hashlib import md5
from flask_login import UserMixin
from datetime import datetime
import jwt
from time import time
from app import app

followers = db.Table(
			"followers",
			db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
			db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
			)


class User(UserMixin,db.Model):
	id = db.Column(db.Integer,primary_key=True) 
	username = db.Column(db.String(30),index=True,unique=True)
	email = db.Column(db.String(30),index=True,unique=True)
	password_hash = db.Column(db.String(30))
	about_me = db.Column(db.String(50))
	last_seen = db.Column(db.DateTime,index=True,default=datetime.utcnow())
	posts = db.relationship('Post',backref='author',lazy='dynamic')
	followed = db.relationship('User',secondary=followers,
			primaryjoin=(followers.c.follower_id==id),secondaryjoin=(followers.c.followed_id==id),
			backref=db.backref('followers',lazy='dynamic'),
			lazy = 'dynamic'
		)

	def __repr__(self):
		return f'<User {self.username}>'

	def set_password(self,password):
		self.password_hash = generate_password_hash(password)


	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def avatar(self,size):
		digest = md5(self.email.encode('utf-8')).hexdigest()
		return f'https://www.gravatar.com/avatar/{digest}?s={size}&d=identicon'

	def follow(self,user):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow(self,user):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following(self,user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id)
		return followed.union(self.posts).order_by(Post.time_stamp.desc())

	def get_reset_password_token(self, expires_in=6000):
		return jwt.encode({'reset-password': self.id, 'exp': time()+expires_in},app.config['SECRET_KEY'],algorithm='HS256').decode('utf-8')	

	@staticmethod
	def verify_reset_password_token(token):
		id = jwt.decode(token, app.config['SECRET_KEY'],algorithm=['HS256'])['reset-password']
		return User.query.get(id)



class Post(db.Model):
	id = db.Column(db.Integer,primary_key=True) 
	body = db.Column(db.String(120))
	time_stamp = db.Column(db.DateTime,index=True,default=datetime.utcnow())
	user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

	def __repr__(self):
		return f'<Post {self.author.username}:{self.body}>'

@login.user_loader  #1)
def user_loader(user_id):
	return User.query.get(int(user_id))



'''#1) user_loader decorator is used to register the function with
Flask-Login, which will call it when it needs to retrieve information about the loggedin user.
The user identifier will be passed as a string, so the function converts it to an
integer before it passes it to the Flask-SQLAlchemy query that loads the user. The
return value of the function must be the user object, or None if the user identifier is
invalid or any other error occurred.'''
