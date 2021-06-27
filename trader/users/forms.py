from flask_wtf.form import FlaskForm
from werkzeug.security import check_password_hash
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from trader.models import User


no_empty = "This field can not be empty"


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(no_empty), Length(min=2, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(no_empty),
            Length(min=4, max=64, message="Password must be 4 to 64 characters long"),
        ],
    )
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(no_empty),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Log In")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User already exists, please try a different one.")


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(no_empty), Length(min=2, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(no_empty),
            Length(min=4, max=64, message="Password must be 4 to 64 characters long"),
        ],
    )
    submit = SubmitField("Log In")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("User doesnot exist, please register a new one.")
    
    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if not check_password_hash(user.hash, password.data):
            raise ValidationError("Password doesnot match!")