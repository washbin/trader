from datetime import datetime

from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from trader import app, db
from trader.models import User, Stock, History
from trader.helpers import apology, login_required, lookup, pass_check


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    hardcash = db.session.query(User).filter_by(id=session["user_id"]).first()
    inspect = db.session.query(Stock).filter_by(user_id=session["user_id"]).all()
    if not inspect:
        return render_template(
            "index.html",
            info=None,
            totalown=hardcash.cash,
            cashown=hardcash.cash,
        )
    else:
        totalown = hardcash.cash
        info = []
        for i in inspect:
            dof = lookup(i.symbol)
            if not dof:
                return apology("uh oh! we have some problem here", 400)
            dof["shares"] = int(i.shares)
            info.append(dof)
            totalown += dof["price"] * i.shares

        return render_template(
            "index.html",
            info=info,
            totalown=totalown,
            cashown=hardcash.cash,
        )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        num = request.form.get("shares")
        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("no such symbol", 400)

        if not num.isnumeric():
            return apology("Invalid shates", 400)

        num = int(num)

        stock_cost = stock["price"]
        if num < 1 or not stock:
            return apology("Cant process that. Check if the shares and symbol is valid")

        availmon = db.session.query(User.cash).filter_by(id=session["user_id"]).all()
        availmon = availmon[0]["cash"]

        if availmon < num * stock_cost:
            return apology("Cant afford that much currently")
        preshare = (
            db.session.query(Stock.shares)
            .filter_by(symbol=stock["symbol"], user_id=session["user_id"])
            .all()
        )
        if not preshare:
            to_add = Stock(
                symbol=stock["symbol"], shares=num, user_id=session["user_id"]
            )
            db.session.add(to_add)
            db.session.commit()
        else:
            to_update = (
                db.session.query(Stock)
                .filter_by(symbol=stock["symbol"], user_id=session["user_id"])
                .first()
            )
            to_update.shares = num + preshare[0]["shares"]
            db.session.commit()

        availmon -= num * stock_cost
        to_update = db.session.query(User).filter_by(id=session["user_id"]).first()
        to_update.cash = availmon
        db.session.commit()

        to_add = History(
            user_id=session["user_id"],
            symbol=stock["symbol"],
            shares=num,
            price=stock_cost,
            transacted=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            event="Bought",
        )
        db.session.add(to_add)
        db.session.commit()
        flash("Stocks purchase successfull")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    histfil = History.query.filter_by(user_id=session["user_id"])
    return render_template("history.html", hist=histfil)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        match_user = (
            db.session.query(User)
            .filter_by(username=request.form.get("username"))
            .first()
        )

        # Ensure username exists and password is correct
        if match_user is None or not check_password_hash(
            match_user.hash, request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = match_user.id

        flash("Login Successfull")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    flash("Succesfully logged out")
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        info = lookup(request.form.get("symbol"))
        if not info:
            return apology("no such symbol", 400)

        return render_template("quoted.html", info=info)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords didnt match", 400)

        # Query database for existing username
        rows = db.session.query(User.username).all()

        # Ensure username not in use
        for row in rows:
            if request.form.get("username") == row["username"]:
                return apology("username already in use", 400)

        # Get password hash
        hashval = generate_password_hash(request.form.get("password"))
        data = User(username=request.form.get("username"), hash=hashval)
        db.session.add(data)
        db.session.commit()

        flash("Registration Successfull, new user created!")
        return redirect("/login", 200)

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        num = int(request.form.get("shares"))
        stock = lookup(request.form.get("symbol"))
        stock_cost = int(stock["price"])
        if num < 1 or not stock:
            return apology("Cant process that. Check if the shares and symbol is valid")

        availmon = db.session.query(User.cash).filter_by(id=session["user_id"]).first()
        availmon = availmon["cash"]

        preshare = (
            db.session.query(Stock.shares)
            .filter_by(symbol=stock["symbol"], user_id=session["user_id"])
            .first()
        )
        if not preshare:
            return apology("Sorry you dont own that stock", 400)
        if num > preshare["shares"]:
            return apology("Sorry you dont own that many stock", 400)
        if num == preshare["shares"]:
            to_delete = (
                db.session.query(Stock)
                .filter_by(symbol=stock["symbol"], user_id=session["user_id"])
                .first()
            )
            db.session.delete(to_delete)
            db.session.commit()
        if num < preshare["shares"]:
            to_update = (
                db.session.query(Stock)
                .filter_by(symbol=stock["symbol"], user_id=session["user_id"])
                .first()
            )
            to_update.shares = preshare["shares"] - num
            db.session.commit()

        availmon += num * stock_cost
        to_update = db.session.query(User).filter_by(id=session["user_id"]).first()
        to_update.cash = availmon
        db.session.commit()

        data = History(
            user_id=session["user_id"],
            symbol=stock["symbol"],
            shares=num,
            price=stock_cost,
            transacted=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            event="Sold",
        )
        db.session.add(data)
        db.session.commit()
        flash("Sold the stocks now you are rich!!")
        return redirect("/")
    else:
        own = db.session.query(Stock.symbol).filter_by(user_id=session["user_id"]).all()
        return render_template("sell.html", stocks=own)
