from flask_login import UserMixin

from trader import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Define models for the tables in database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    hash = db.Column(db.String(256), nullable=False)
    cash = db.Column(db.Integer, default=10000.0)

    def __repr__(self) -> str:
        return f"User {self.username}"


class Stock(db.Model):
    stock_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Stock {self.symbol}"


class History(db.Model):
    hist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    transacted = db.Column(db.String(128), nullable=False)
    event = db.Column(db.String(10), nullable=False)

    def __repr__(self) -> str:
        return f"History number: {self.hist_id}"
