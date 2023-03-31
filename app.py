import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    cash = rows[0]["cash"]

    # Get user portfolio
    portfolio = db.execute("""SELECT symbol, name, SUM(shares) as sum_of_shares FROM transactions WHERE user_id = ?
                           GROUP BY user_id, symbol, name HAVING sum_of_shares > 0""", session["user_id"])

    # Use lookup API to get current price for each stock
    portfolio = [dict(x, **{'price': lookup(x['symbol'])['price']}) for x in portfolio]

    # Use lookup API to get correct symbol for each stock
    portfolio = [dict(x, **{'symbol': lookup(x['symbol'])['symbol']}) for x in portfolio]

    # Calculate total price for each stock
    portfolio = [dict(x, **{'total': x['price']*x['sum_of_shares']}) for x in portfolio]

    total = cash + sum([x['total'] for x in portfolio])

    return render_template("index.html", cash=cash, portfolios=portfolio, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # POST
    if request.method == "POST":

        # Ensure symbol was submitted
        if not (symbol := request.form.get("symbol")):
            return apology("missing symbol", 400)

        # Ensure shares was submitted
        if not (shares := request.form.get("shares")):
            return apology("missing shares", 400)

        # Check share is numeric
        try:
            shares = int(shares)
        except ValueError:
            return apology("invalid shares", 400)

        # Ensure symbol is valid
        if (quote := lookup(symbol)) == None:
            return apology("invalid symbol", 400)

        # Ensure valid amount of shares
        if shares < 0:
            return apology("invalid amount of shares", 400)

        # Ensure user has enough cash to afford the stock
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]
        total_price = shares * (price := quote['price'])

        if cash < total_price:
            return apology("can't afford", 400)

        # Run SQL statement on database to purchase stock
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], quote["name"], shares, price)

        # Update cash to reflect purchased stock
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   (cash - total_price), session["user_id"])

        flash("Bought!")

        return redirect("/")

    # GET
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get transactions
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # POST
    if request.method == "POST":

        # Look up stock
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("invalid symbol", 400)

        else:

            # Format price
            quote['price'] = usd(quote['price'])

            # Render result
            return render_template("quoted.html", quote=quote)

    # GET
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not confirmation:
            return apology("must provide password confirmation", 400)

        # Ensure password and confirmation match
        elif password != confirmation:
            return apology("passwords don't match", 400)

        # Ensure username doesn't exist
        if len(db.execute("SELECT * FROM users WHERE username = ?", username)) != 0:
            return apology("username is taken", 400)

        # Remember user
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash("Registered!")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # POST
    if request.method == "POST":
        # Ensure symbol was submitted
        if not (symbol := request.form.get("symbol")):
            return apology("missing symbol", 400)

        # Ensure shares was submitted
        if not (shares := request.form.get("shares")):
            return apology("missing shares", 400)

        # Check share is numeric
        try:
            shares = int(shares)
        except ValueError:
            return apology("invalid shares", 400)

        # Ensure symbol is valid
        if (quote := lookup(symbol)) == None:
            return apology("invalid symbol", 400)

        # Ensure valid amount of shares
        if shares < 0:
            return apology("invalid amount of shares", 400)

        # Ensure user has enough shares to sell
        total_shares = db.execute("""SELECT SUM(shares) as total_shares FROM transactions WHERE symbol = ?""", quote["symbol"])
        if shares > total_shares[0]["total_shares"]:
            return apology("too many shares", 400)

        # Run SQL statement on database to sell stock
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], quote["symbol"], quote["name"], -shares, price := quote['price'])

        # Update cash to reflect purchased stock
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash = rows[0]["cash"]
        total_price = shares * price
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   (cash + total_price), session["user_id"])

        flash("Sold!")

        return redirect("/")

    # GET
    else:

        # Get symbols
        symbols = db.execute("SELECT DISTINCT(symbol) FROM transactions WHERE user_id = ?", session["user_id"])

        return render_template("sell.html", symbols=symbols)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add cash to account"""

    # POST
    if request.method == "POST":

        # Ensure cash was submitted
        if not (cash_deposit := request.form.get("cash")):
            return apology("missing cash", 400)

        # Ensure password was submitted
        if not (password := request.form.get("password")):
            return apology("must provide password", 400)

         # Check cash is numeric
        try:
            cash_deposit = int(cash_deposit)
        except ValueError:
            return apology("invalid cash", 400)

        # Ensure valid cash
        if cash_deposit < 0:
            return apology("invalid cash", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure username exists and password is correct
        if not check_password_hash(rows[0]["hash"], password):
            return apology("invalid password", 400)

        # Get cash from account
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        cash_account = rows[0]["cash"]

        # Add cash to account
        cash = cash_account + cash_deposit
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])

        flash("Cash added!")

        return redirect("/")

    # GET
    else:
        return render_template("add_cash.html")