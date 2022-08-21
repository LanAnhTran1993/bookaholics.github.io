from crypt import methods
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
from flask_session import Session

from flask import redirect, render_template, request, session
from functools import wraps
import json
import ast

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

#Define login_required function
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    connection = sqlite3.connect("users.db", check_same_thread=False)
    crsr = connection.cursor()
    if request.method == "POST":
        crsr.execute("SELECT name FROM users;")
        usernames = crsr.fetchall()
        names = [i[0] for i in usernames]
        if request.method == "POST":
            name = request.form.get("username")
            password = request.form.get("password")
            password_confirmation = request.form.get("confirmation")
            password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            crsr.execute("INSERT INTO users (name, hash) VALUES (?, ?)", (name, password))
            connection.commit()
            return render_template("login.html")
    else:
        return render_template("register.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # Ensure username was submitted
    if not request.form.get("username"):
        return render_template("apology.html", bottom="Must provide a username.")

    # Ensure password was submitted
    elif not request.form.get("password"):
        return render_template("apology.html", bottom="Must provide a username.")

    # Query database for username
    connection = sqlite3.connect("users.db", check_same_thread=False)
    crsr = connection.cursor()
    crsr.execute("SELECT * FROM users WHERE name = ?", [request.form.get("username")])
    rows = [{'id': col1, 'name': col2, 'hash': col3} for (col1, col2, col3) in crsr.fetchall()]
    # Ensure username exists and password is correct
    if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        return render_template("apology.html", bottom="Must provide a username.")

    # Remember which user has logged in
    session["user_id"] = rows[0]["id"]

    # Redirect user to home page
    return render_template("loggedin.html")

@app.route("/logout")
@login_required
def logout():

    """Log user out"""
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
        
@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    connection = sqlite3.connect("users.db", check_same_thread=False)
    crsr = connection.cursor()
    if request.method == "POST":
        userid = session["user_id"]
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        duration = request.form.get("duration")
        review = request.form.get("review")
        rating = int(request.form.get("rate"))
        crsr.execute("INSERT INTO entries (title, author, genre, userid, duration, review, rating) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, author, genre, userid, duration, review, rating))
        connection.commit()
        connection.close()
        return redirect("/past")
    elif request.method == "GET":
        return render_template("new.html")

@app.route("/past", methods=["GET", "POST"])
@login_required
def past():
    connection = sqlite3.connect("users.db", check_same_thread=False)
    crsr = connection.cursor()
    userid = session["user_id"]
    crsr.execute("SELECT title, author, genre, duration, SUBSTRING(review, 1, 100), date, id, rating FROM entries WHERE userid = ? ORDER BY date", [userid])
    rows = [{'title': col1, 'author': col2, 'genre': col3, 'duration': col4, 'review': col5, 'date': col6, 'id': col7, "rating": col8} for (col1, col2, col3, col4, col5, col6, col7, col8) in crsr.fetchall()]
    connection.close()
    return render_template("past.html", rows = rows, message = "YOU HAVE READ THIS MANY BOOKS. CONGRATULATIONS")

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    connection = sqlite3.connect("users.db", check_same_thread=False)
    crsr = connection.cursor()
    userid = session["user_id"]
    search = request.form.get("search")
    crsr.execute("SELECT title, author, genre, duration, SUBSTRING(review, 1, 100), date, id, rating FROM entries WHERE userid = ? AND title  LIKE ?", (userid, '%'+search+'%'))
    rows = [{'title': col1, 'author': col2, 'genre': col3, 'duration': col4, 'review': col5, 'date': col6, 'id': col7, 'rating': col8} for (col1, col2, col3, col4, col5, col6, col7, col8) in crsr.fetchall()]
    return render_template("past.html", rows = rows, message = "SEARCH RESULTS")

@app.route("/random", methods=["GET", "POST"])
@login_required
def random():
    connection = sqlite3.connect("users.db", check_same_thread=False)
    crsr = connection.cursor()
    userid = session["user_id"]
    crsr.execute("SELECT title, author, genre, duration, SUBSTRING(review, 1, 100), date, id, rating FROM entries ORDER BY RANDOM()")
    rows = [{'title': col1, 'author': col2, 'genre': col3, 'duration': col4, 'review': col5, 'date': col6, 'id': col7, 'rating': col8} for (col1, col2, col3, col4, col5, col6, col7, col8) in crsr.fetchall()]
    return render_template("past.html", rows = rows, message = "THESE ARE WHAT USERS HAVE READ")

@app.route("/entry", methods=["GET", "POST"])
@login_required
def entry():
    connection = sqlite3.connect("users.db", check_same_thread=False)
    crsr = connection.cursor()
    form = (request.form.get("id"))
    row = ast.literal_eval(form)
    id = row["id"]
    crsr.execute("SELECT title, author, genre, duration, review, date, rating FROM entries WHERE id=?", [id])
    row = [{'title': col1, 'author': col2, 'genre': col3, 'duration': col4, 'review': col5, 'date': col6, 'rating': col7} for (col1, col2, col3, col4, col5, col6, col7) in crsr.fetchall()]
    return render_template("entry.html", row = row)

@app.route("/loggedin", methods=["GET", "POST"])
def loggedin():
    return render_template("loggedin.html")