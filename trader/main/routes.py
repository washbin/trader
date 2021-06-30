from flask import Blueprint
from flask.templating import render_template
from flask_login import current_user
from flask_login.utils import login_required

from trader.models import History, Stock, User
from trader.utils import lookup


main = Blueprint("main", __name__)


@main.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash_money = User.query.filter_by(id=current_user.id).first()
    cash_money = cash_money.cash
    all_stocks = Stock.query.filter_by(user_id=current_user.id).all()
    if not all_stocks:
        return render_template(
            "index.html",
            info=None,
            total_owned=cash_money,
            cash_owned=cash_money,
        )
    else:
        total_owned = cash_money
        info = []
        for stock in all_stocks:
            stock_info = lookup(stock.symbol)
            if not stock_info:
                return (
                    render_template(
                        "apology.html",
                        title="Apology",
                        top=400,
                        bottom="Uh oh! We seem to have some problem here",
                    ),
                    400,
                )

            stock_info["shares"] = int(stock.shares)
            info.append(stock_info)
            total_owned += stock_info["price"] * stock.shares

        return render_template(
            "index.html",
            title="Home",
            info=info,
            total_owned=total_owned,
            cash_owned=cash_money,
        )


@main.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histfil = History.query.filter_by(user_id=current_user.id)
    return render_template("history.html", title="History", hist=histfil)
