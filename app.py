import os

from flask import Flask, request, jsonify, render_template, redirect, session
from cs50 import SQL
from helpers import login_required
from error import apology
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///alpha.db")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
@login_required
def home():
    return render_template('index.html')



@app.route("/decoded", methods=["GET", "POST"])
@login_required
def decoded():
    # msg = list(request.form.values())
    #import os
    # if os.path.exists("static/result/temp.png"):
        #print("YESSSSSS")
    # os.remove("static/result/temp.png")
    msg = [str(i) for i in request.form.values()]
    print(msg)
    x, key = msg[0], msg[1]
    from model import eval
    e = eval()

    ret_message, total_cost_dict, loc_list = e.run(x, key)

    if ret_message == None:
        return apology("NA TRY AGAIN", 400)
    else:
        camps = []
        total_cost_list = []

        for camp, total_cost in total_cost_dict.items():
            if camp not in loc_list:
                camps.append(camp)
                total_cost_list.append(total_cost)

        return render_template("decoded_msg.html", solution_text=ret_message, camps=camps, total_cost_list=total_cost_list, legend="Cost (Total Distance)")



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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        rows = db.execute("SELECT * from users where username = :username",
        username = request.form.get("username"))

        if len(rows) == 1 or not request.form.get("username"):
            return apology("Username invalid!")

        elif not request.form.get("password"):
            return apology("Please enter password!")

        elif request.form.get("password") != request.form.get("password(again)"):
            return apology("The two passwords do not match!")

        username = request.form.get("username")
        password = request.form.get("password")

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=generate_password_hash(password))

        return redirect("/")


@app.route("/encrypt", methods=["GET", "POST"])
@login_required
def encrypt():

    if request.method == "POST":
        from encoder import message_encoder

        message_encoder = message_encoder()

        msg = [str(i) for i in request.form.values()]
        print(msg)
        x, key = msg[0], msg[1]

        ret = message_encoder.encode_message(x, key)

        print(ret)

        return render_template("encrypt_answer.html", solution_text=ret)
    else:
        return render_template("encrypt.html")


if __name__ == "__main__":
    app.run(debug=True)
