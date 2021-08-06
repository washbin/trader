from datetime import datetime

from flask import Blueprint, request
from flask.helpers import flash, url_for
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.utils import redirect

from trader import db
from trader.models import History, Stock, User
from trader.stocks.forms import BuyForm, QuoteForm, SellForm
from trader.utils import lookup


stocks = Blueprint("stocks", __name__)


@stocks.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    form = QuoteForm()
    if form.validate_on_submit():
        info = lookup(request.form.get("symbol"))
        return render_template(
            "quote.html",
            title="quote",
            info=info,
        )

    else:
        return render_template("quote.html", title="quote", info=None, form=form)


@stocks.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    form = BuyForm()
    if form.validate_on_submit():
        num = int(request.form.get("shares"))
        stock = lookup(request.form.get("symbol"))
        stock_cost = stock["price"]

        availmon = User.query.filter_by(id=current_user.id).first().cash

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
        return render_template("buy.html", title="Buy", form=form)


@stocks.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    form = SellForm()
    if form.validate_on_submit():
        num = int(request.form.get("shares"))
        stock = lookup(request.form.get("symbol"))
        stock_cost = float(stock["price"])

        availmon = User.query.filter_by(id=current_user.id).first().cash

        preshare = Stock.query.filter_by(
            symbol=stock["symbol"], user_id=current_user.id
        ).first()

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
        form.symbol.choices = list(
            map(
                lambda x: (x.symbol, x.symbol),
                Stock.query.filter_by(user_id=current_user.id).all(),
            )
        )
        return render_template("sell.html", title="Buy", form=form)
