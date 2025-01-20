import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    if request.method == "GET":

        """ Query stock_portfolio for company, symbol and shares_owned"""
        index = db.execute("SELECT company, symbol, shares_owned FROM stock_portfolio WHERE user_id = :user_id", user_id=session["user_id"])

        total_stockvalue = 0

        """Query current stock price for all symbols in user's stock_portfolio"""
        for dic in index:
            symbol = dic["symbol"]
            quote, error = get_quote(symbol)
            if error:
                return apology("Error fetching stock price", 400)

            dic["price"] = quote["price"]
            dic["price"] = float(dic["price"])

            """Caulculate symbol's individual stock value totals"""
            dic["total_value"] = quote["price"] * dic["shares_owned"]

            total_stockvalue += float(dic["total_value"])

        """Calculate total sum of shares owned"""
        total_cash = db.execute("SELECT cash FROM users WHERE id=:user_id", user_id=session["user_id"])
        total_cashbalance = float(total_cash[0]["cash"])

        """Calculate grand total = cash + stock value"""

        grand_total = total_cashbalance + total_stockvalue
        print(f"total_cash: {total_cashbalance}, grand_total: {grand_total}")

        return render_template("index.html", index=index, total_cash=total_cashbalance, grand_total=grand_total)

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method=="POST":
        old_password = request.form.get("old_password")
        if not old_password or old_password.isspace():
            return apology("Please insert old password", 400)
        old_password_hash = db.execute("SELECT hash FROM users WHERE id=:user_id", user_id=session["user_id"])
        if not check_password_hash(old_password_hash[0]["hash"], old_password):
            return apology("Please insert correct old password", 400)
        password = request.form.get("password")
        if not password or password.isspace():
            return apology("Please insert new password", 400)
        confirm_password = request.form.get("confirm_password")
        if not password or password.isspace():
            return apology("Please insert new password", 400)
        if password != confirm_password:
            return apology("New password and its confirmation do not match", 400)
        hash_new_password = generate_password_hash("password")

        db.execute("UPDATE users SET hash = :hash_new_password WHERE id=:user_id", user_id=session["user_id"], hash_new_password = hash_new_password)

        return render_template("index.html")
    else:
        return render_template("settings.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        """ Request shares and amount"""
        quote_entry = request.form.get("symbol")
        if not quote_entry or quote_entry.isspace():
            return apology("Provide valid quite syntax", 400)
        amount_shares = request.form.get("shares")
        if not amount_shares or amount_shares.isspace() or not amount_shares.isdigit() or int(amount_shares) <= 0:
            return apology("Provide a valid number of shares", 400)
        quote, error = get_quote(quote_entry)

        if error:
            return apology("Insert correct quote", 400)

        """Calculate cost of share requested"""
        cost = int(amount_shares) * float(quote["price"])

        """Check if user has enough money"""
        bankroll_sql = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
        bankroll = float(bankroll_sql[0]['cash'])

        if cost > bankroll:
            return apology("insufficient funds on account", 400)

        """Complete buy"""
        new_account_balance = bankroll - cost
        db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id",
                   user_id = session["user_id"], new_balance = new_account_balance)
        db.execute("INSERT INTO buy (user_id, company, symbol, amount, share_price, total, timestamp) VALUES (:user_id, :company, :symbol, :amount_shares, :share_price, :cost, CURRENT_TIMESTAMP)",
                   user_id = session["user_id"], company = quote["name"], symbol = quote_entry, amount_shares = amount_shares, share_price = quote["price"], cost = cost)

        """Update the stock_portfolio table of the user accordingly"""
        result = db.execute("SELECT symbol FROM stock_portfolio WHERE user_id = :user_id AND symbol = :symbol", user_id = session["user_id"], symbol = quote_entry)
        if len(result) == 0:
            db.execute("INSERT INTO stock_portfolio (user_id, company, symbol, shares_owned) VALUES (:user_id, :company, :symbol, :shares_owned)",
                        user_id=session["user_id"], company = quote["name"], symbol = quote_entry, shares_owned = amount_shares)
        else:
            db.execute("UPDATE stock_portfolio SET shares_owned = shares_owned + :amount_shares WHERE user_id = :user_id AND symbol = :symbol",
                        amount_shares = amount_shares, symbol = quote_entry, user_id = session["user_id"])

        return redirect(url_for('index'))

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("""SELECT company, symbol, amount, total, timestamp, 'purchase' AS transaction_type FROM buy WHERE user_id= :user_id UNION ALL SELECT company, symbol, amount, total, timestamp, 'sale' AS transaction_type FROM sell WHERE user_id= :user_id ORDER BY timestamp""", user_id=session["user_id"])
    print(history)
    return render_template("history.html", history=history)




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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "POST":
        quote_entry = request.form.get("symbol")

        if not quote_entry or quote_entry.isspace():
            return apology("Please enter a valid quote", 400)

        quote, error = get_quote(quote_entry)
        print(quote)
        if error:
            return apology("Quote not found", 400)


        return render_template("quoted.html", name=quote["name"], price=quote["price"], symbol=quote["symbol"])

    else:
       return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        if not username or username.isspace():
            return apology("Please provide a username", 400)
        list_usernames = db.execute("SELECT username FROM users")
        for names in list_usernames:
            if username == names["username"]:
                return apology("username already exists", 400)
        password = request.form.get("password")
        if not password or password.isspace():
            return apology("Please provide a password", 400)
        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return apology("Confirmation not identical to password", 400)

        hash_password = generate_password_hash(confirmation)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                    username, hash_password)

        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        """Confirming correct input"""
        quote_entry = request.form.get("symbol")
        confirm_select = db.execute("SELECT symbol FROM stock_portfolio WHERE user_id= :user_id AND symbol= :symbol", user_id=session["user_id"], symbol=quote_entry)
        if len(confirm_select) == None:
            return apology("You don't own that stock", 400)
        if not quote_entry or quote_entry.isspace():
            return apology("Please enter a stock symbol", 400)
        amount = request.form.get("shares")
        bankroll_sql = db.execute("SELECT shares_owned FROM stock_portfolio WHERE user_id= :user_id AND symbol= :symbol", user_id=session["user_id"], symbol=quote_entry)
        if int(bankroll_sql[0]['shares_owned']) < int(amount):
            return apology("You don't own that many shares", 400)
        if not quote_entry or quote_entry.isspace() or int(amount) < 0:
            return apology("Input invalid - no negatives or empty inputs", 400)

        """Calculate the revenue of sale"""
        quote, error = get_quote(quote_entry)
        if error:
            return apology("Insert correct quote", 400)

        revenue_sale = int(amount) * float(quote['price'])
        revenue_sale = revenue_sale

        """Update data base tables: sell, stock_portfolio and user(cash)"""

        """Update user cash & sell"""

        bankroll_sql = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
        bankroll = int(bankroll_sql[0]['cash'])
        new_account_balance = bankroll + revenue_sale
        db.execute("UPDATE users SET cash = :new_balance WHERE id = :user_id",
                   user_id = session["user_id"], new_balance = new_account_balance)
        db.execute("INSERT INTO sell (user_id, company, symbol, amount, share_price, total, timestamp) VALUES (:user_id, :company, :symbol, :amount_shares, :share_price, :cost, CURRENT_TIMESTAMP)",
                   user_id = session["user_id"], company = quote["name"], symbol = quote_entry, amount_shares = amount, share_price = quote["price"], cost = revenue_sale)

        """Update user stock_portfolio"""
        db.execute("UPDATE stock_portfolio SET shares_owned = shares_owned - :amount_shares WHERE user_id = :user_id AND symbol = :symbol",
                        amount_shares = amount, symbol = quote_entry, user_id = session["user_id"])

        return redirect(url_for('index'))
    else:
        if request.method == "GET":
            symbols=db.execute("SELECT symbol FROM stock_portfolio WHERE user_id=:user_id", user_id=session["user_id"])

        return render_template("sell.html", symbols=symbols)


def get_quote(symbol):

    """Get stock quote."""
    quote = lookup(symbol)

    if not quote:
        return None, "Quote not found"

    return {
        "name": quote["name"],
        "price": quote["price"],
        "symbol": quote["symbol"]
    }, None

