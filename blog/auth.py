from flask import current_app, g, Blueprint, session, redirect, url_for, request, render_template
from . import db
import functools
from .forms import LoginForm, RegistrationForm

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None if user_id is None else db.get_user_by_id(user_id)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        return redirect(url_for('auth.login')) if g.user is None else view(**kwargs)
    return wrapped_view


@auth.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)

    if (request.method == 'POST' and form.validate()):
        if user := db.login(form.username.data, form.password.data):
            g.user = user
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog.index'))
        else:
            form.username.errors = ("invalid username or password", )
            form.password.errors = ("invalid username or password", )

    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        if db.new_user(form.username.data, form.password.data):
            return redirect(url_for('auth.login'))
        else:
            form.username.errors = ("Username already taken", )
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
def logout():
    session.pop("user_id")
    g.user = None
    return redirect(url_for('blog.index'))