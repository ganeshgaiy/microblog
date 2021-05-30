from app import app,db
from datetime import datetime
from snippets import is_safe_url
from flask_login import login_required,login_user,current_user,logout_user
from flask import render_template,url_for,redirect,flash,request
from app.forms import LoginForm, RegisterForm,PostForm,EditProfileForm,ForgotPasswordForm,ResetPasswordForm
from app.models import User,Post
from app.email import send_pass_request_email

@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()

@app.route('/',methods=['GET','POST'])
@app.route('/index',methods=['GET','POST'])
@login_required
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.user_post.data,author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Posted successfully')
		return redirect(url_for('index'))
	page = request.args.get('page',1,type=int)
	posts = current_user.followed_posts().paginate(page,app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('index',page=posts.next_num) if posts.has_next else None
	prev_url = url_for('index',page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html',title='Home',form=form,posts=posts.items,next_url=next_url,prev_url=prev_url)

@app.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.check_password(form.password.data):
			login_user(user,remember=form.remember_me.data)  #1) Flask-Login’s login_user() function is invoked to record the user as logged in for the user session. 
			next_page = request.args.get('next')
			if next_page is None or is_safe_url(next_page)==False:
				return redirect(url_for('index'))
			else:
				return redirect(next_page)
		flash('Invalid Username or password')
	return render_template('login.html',title='login',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data,email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Success! You are now a registered user')
		return redirect(url_for('login'))
	return render_template('register.html',title='register', form=form)

@app.route('/logout')
def logout():
	if current_user.is_anonymous:
		return redirect(url_for('login'))
	if current_user.is_authenticated:
		logout_user()
		return redirect(url_for('login'))

# @app.route('/forgot_password',methods=['GET','POST'])
# def forgot_password():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('index'))
# 	form = ForgotPasswordForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter(User.email == form.email.data).first()
# 		if user is None:
# 			flash('No user with such email address exists')
# 			# return redirect(url_for('forgot_password'))
# 			return render_template('reset_pass_request.html',title='Reset Password',form=form)
# 		send_pass_request_email(user)  #
# 		flash("A email has been sent to your registered email id")
# 		return redirect(url_for('login'))
# 	return render_template('reset_pass_request.html',title='Reset Password',form=form)

# @app.route('/reset_password/<token>',methods=['GET','POST'])
# def reset_password(token):
# 	if current_user.is_authenticated:
# 		return redirect(url_for('index'))
# 	user = User.verify_reset_password_token(token)
# 	# user = User.query.get(user_id)
# 	if not user:
# 		# flash("sorry!")
# 		return redirect(url_for('index'))
# 	form = ResetPasswordForm()
# 	if form.validate_on_submit():
# 		user.set_password(form.password.data)	
# 		db.session.commit()
# 		flash("Your password has been reset.")
# 		return redirect(url_for('login'))
# 	return render_template('reset_password.html',form=form,title='reset_password',user=user)



@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_pass_request_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_pass_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    # if request.method == 'GET':
    # 	flash("this is post and not working")
    return render_template('reset_password.html', form=form,title='reset_password')




@app.route('/profile/<username>')
@login_required
def profile(username):
	user  = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page',1,type=int)
	posts = user.posts.order_by(Post.time_stamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('profile',username=username,page=posts.next_num) if posts.has_next else None
	prev_url = url_for('profile',username=username,page=posts.prev_num) if posts.has_prev else None
	return render_template('profile.html',username=username,user=user,title='profile',posts=posts.items,next_url=next_url,prev_url=prev_url)


@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('you changes have been saved')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html',form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash(f'user {username} not found')
		return redirect(url_for('index'))
	if user==current_user:
		flash('you cannot follow yourself')
	if current_user.is_following(user):
		current_user.unfollow(user)
		db.session.commit()
	else:
		current_user.follow(user)
		db.session.commit()
	return redirect(url_for('profile',username=username))

@app.route('/explore')
@login_required
def explore():
	page = request.args.get('page',1,type=int)
	posts = Post.query.order_by(Post.time_stamp.desc()).paginate(page,app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('explore',page=posts.next_num) if posts.has_next else None
	prev_url = url_for('explore',page=posts.prev_num) if posts.has_prev else None
	return render_template('explore.html',posts=posts.items,next_url=next_url,prev_url=prev_url,title='explore')

