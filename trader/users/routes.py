from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import login_required
from flask_login.utils import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from trader import db
from trader.models import User
from trader.utils import apology
from trader.users.forms import LoginForm, RegisterForm


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegisterForm()
    # if request.method == "POST" and form.is_submitted() and form.validate():
    if form.validate_on_submit():
        # Query database for existing username
        rows = db.session.query(User.username).all()
        # Ensure requested username not in use
        for row in rows:
            if request.form.get("username") == row["username"]:
                return apology("username already in use", 400)

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
    # User reached route via POST (as by submitting a form via POST)
    if form.validate_on_submit():
        # Query database for username
        user = db.session.query(User).filter_by(username=form.username.data).first()

        # Ensure username exists and password is correct
        if user and check_password_hash(user.hash, form.password.data):
            # Remember which user has logged in
            login_user(user)

            flash("Logged in Successfully.", "success")

            next = request.args.get("next")

            # Redirect user to home page
            return redirect(next or url_for("main.index"))

        return apology("invalid username and/or password", 403)

    # User reached route via GET (as by clicking a link or via redirect)
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
