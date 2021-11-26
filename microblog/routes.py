"""
Routes
"""
from flask import render_template, flash, redirect, url_for, Blueprint
# from microblog.app import app
from .forms import LoginForm

bp = Blueprint('app', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    user = {'username': 'Miguel'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect(url_for('app.index'))
    return render_template('login.html', title='Sign In', form=form)