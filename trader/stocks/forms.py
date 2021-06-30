from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.fields.core import IntegerField, SelectField, StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError

from trader.models import Stock, User
from trader.utils import lookup


class QuoteForm(FlaskForm):
    symbol = StringField("Symbol", validators=[DataRequired()])
    submit = SubmitField("Quote")

    def validate_symbol(self, symbol):
        if not lookup(symbol.data):
            raise ValidationError("No such symbol exists in our database!")


class BuyForm(FlaskForm):
    symbol = StringField("Symbol", validators=[DataRequired()])
    shares = IntegerField(
        "Shares",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="You cannot buy less than 1 stock"),
        ],
    )
    submit = SubmitField("Buy")

    def validate_symbol(self, symbol):
        if not lookup(symbol.data):
            raise ValidationError("No such symbol exists in our database!")

    def validate_shares(self, shares):
        data = lookup(self.symbol.data) or {"price": 1}
        if (
            User.query.filter_by(id=current_user.id).first().cash
            < data["price"] * shares.data
        ):
            raise ValidationError("You dont have enough money to buy that many")


class NewSelectField(SelectField):
    def pre_validate(self, form):
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class SellForm(FlaskForm):
    symbol = NewSelectField(label="Symbol", coerce=str, validators=[DataRequired()])
    shares = IntegerField(
        "Shares",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="You cannot sell less than 1 stock"),
        ],
    )
    submit = SubmitField("Sell")

    def validate_shares(self, shares):
        if (
            Stock.query.filter_by(symbol=self.symbol.data, user_id=current_user.id)
            .first()
            .shares
            < shares.data
        ):
            raise ValidationError("You dont own that many of that stock")
