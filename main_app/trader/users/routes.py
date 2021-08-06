from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import login_required
from flask_login.utils import login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from trader import db
from trader.models import User
from trader.users.forms import LoginForm, RegisterForm


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegisterForm()

    if form.validate_on_submit():

        # Get password hash
        password_hash = generate_password_hash(request.form.get("password"))
        # Create new entry in database
        new_user = User(username=request.form.get("username"), hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("New user registered succesfully!", "success")
        return redirect(url_for("users.login"), 200)

    else:
        return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    logout_user()
    form = LoginForm()

    if form.validate_on_submit():

        # Remember which user has logged in
        login_user(User.query.filter_by(username=form.username.data).first())
        flash("Logged in Successfully.", "success")
        next = request.args.get("next")
        # Redirect user to next page or home page
        return redirect(next or url_for("main.index"))

    else:
        return render_template("login.html", title="Log In", form=form)


@users.route("/logout")
@login_required
def logout():
    """Log user out"""
    logout_user()
    flash("Succesfully logged out", "success")
    # Redirect user to login form
    return redirect(url_for("users.login"))
