from trader import db

# Define models for the tables in database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    hash = db.Column(db.String(256), nullable=False)
    cash = db.Column(db.Integer, default=10000.0)


class Stock(db.Model):
    stock_id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class History(db.Model):
    hist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    transacted = db.Column(db.String(128), nullable=False)
    event = db.Column(db.String(10), nullable=False)
