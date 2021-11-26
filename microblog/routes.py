"""
Views
"""
from datetime import datetime
from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from microblog.forms import LoginForm, RegistrationForm, EditProfileForm
from microblog.models import User
from microblog.extensions import db

bp = Blueprint('user', __name__)

@bp.before_request
def set_last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('user.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        
        # Redirect to index if next url is a full url instead of relative
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('user.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('edit_profile')
@login_required
def edit_profile():
    form = EditProfileForm()
    
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        current_user.username = form.username.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    
    return render_template('edit_profile.html', form=form, title='Edit Profile')

@bp.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('profile.html', user=user, posts=posts)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.index'))