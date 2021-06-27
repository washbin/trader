from datetime import datetime

from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.utils import redirect

from trader import db
from trader.models import History, Stock, User
from trader.utils import apology, lookup


stocks = Blueprint("stocks", __name__)


@stocks.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        info = lookup(request.form.get("symbol"))
        if not info:
            return apology("no such symbol", 400)

        return render_template("quote.html", title="quote", info=info)

    else:
        return render_template("quote.html", title="quote", info=None)


@stocks.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        num = request.form.get("shares")
        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("no such symbol", 400)

        if not num.isnumeric():
            return apology("Invalid shares", 400)

        num = int(num)

        stock_cost = stock["price"]
        if num < 1 or not stock:
            return apology("Cant process that. Check if the shares and symbol is valid")

        availmon = User.query.filter_by(id=current_user.id).first()
        availmon = availmon.cash

        if availmon < num * stock_cost:
            return apology("Cant afford that much currently")
        preshare = Stock.query.filter_by(
            symbol=stock["symbol"], user_id=current_user.id
        ).first()
        if not preshare:
            to_add = Stock(symbol=stock["symbol"], shares=num, user_id=current_user.id)
            db.session.add(to_add)
            db.session.commit()
        else:
            to_update = Stock.query.filter_by(
                symbol=stock["symbol"], user_id=current_user.id
            ).first()
            to_update.shares = num + preshare.shares
            db.session.commit()

        availmon -= num * stock_cost
        to_update = User.query.filter_by(id=current_user.id).first()
        to_update.cash = availmon
        db.session.commit()

        to_add = History(
            user_id=current_user.id,
            symbol=stock["symbol"],
            shares=num,
            price=stock_cost,
            transacted=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            event="Bought",
        )
        db.session.add(to_add)
        db.session.commit()
        flash("Stocks purchased successfully", "success")
        return redirect(url_for("main.index"))
    else:
        return render_template("buy.html", title="Buy")


@stocks.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        num = int(request.form.get("shares"))
        stock = lookup(request.form.get("symbol"))
        stock_cost = int(stock["price"])
        if num < 1 or not stock:
            return apology("Cant process that. Check if the shares and symbol is valid")

        availmon = User.query.filter_by(id=current_user.id).first()
        availmon = availmon.cash

        preshare = Stock.query.filter_by(
            symbol=stock["symbol"], user_id=current_user.id
        ).first()
        if not preshare:
            return apology("Sorry you dont own that stock", 400)
        if num > preshare.shares:
            return apology("Sorry you dont own that many stock", 400)
        if num == preshare.shares:
            to_delete = Stock.query.filter_by(
                symbol=stock["symbol"], user_id=current_user.id
            ).first()
            db.session.delete(to_delete)
            db.session.commit()
        if num < preshare.shares:
            to_update = Stock.query.filter_by(
                symbol=stock["symbol"], user_id=current_user.id
            ).first()
            to_update.shares = preshare.shares - num
            db.session.commit()

        availmon += num * stock_cost
        to_update = User.query.filter_by(id=current_user.id).first()
        to_update.cash = availmon
        db.session.commit()

        data = History(
            user_id=current_user.id,
            symbol=stock["symbol"],
            shares=num,
            price=stock_cost,
            transacted=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            event="Sold",
        )
        db.session.add(data)
        db.session.commit()
        flash("Sold the stocks now you are rich!!", "success")
        return redirect(url_for("main.index"))
    else:
        own = Stock.query.filter_by(user_id=current_user.id).all()
        return render_template("sell.html", title="Buy", stocks=own)
