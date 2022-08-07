import os
import secrets
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from werkzeug.utils import secure_filename

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Displays the main page
@app.route("/")
def index():
    """Show news"""
    # Get data from the database
    news = db.execute("SELECT news.id, datetime, username, header, image, text FROM news JOIN users ON users.id = news.users_id ORDER BY datetime DESC")
    for element in news:
        element["image_path"] = url_for('static', filename=element["image"])
    return render_template("index.html", news=news)

# To enter the site
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Must fill in the username field!', 'danger')
            return render_template ("login.html")


        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Must fill in the password field!', 'danger')
            return render_template ("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash('Incorrect password or username!', 'danger')
            return render_template ("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# To exit the site
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# To register on the site
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        hash = generate_password_hash(request.form.get("password"))
        email = request.form.get("email")
        usernames = db.execute("SELECT username FROM users")

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Must fill in the username field!', 'danger')
            return render_template ("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Must fill in the password field!', 'danger')
            return render_template ("register.html")

        # Ensure password_again was submitted
        elif not request.form.get("confirmation"):
            flash('Must fill in the password (again) field!', 'danger')
            return render_template ("register.html")

        if request.form.get("password") != request.form.get("confirmation"):
            flash('Your passwords do not match!', 'danger')
            return render_template ("register.html")

        for dictionary in usernames:
            if (dictionary["username"]) == username:
                flash('This username already exists!', 'danger')
                return render_template ("register.html")

        db.execute("INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", username, hash, email)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Remember which user
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

# To publish news on the site
@app.route("/add_news", methods=["GET", "POST"])
@login_required
def add_news():
    if request.method == "POST":
        if not request.form.get("header"):
            flash('Must fill in the header field!', 'danger')
            return render_template ("add_news.html")
        if not request.form.get("text"):
            flash('Must fill in the text field!', 'danger')
            return render_template ("add_news.html")

        header = request.form.get("header")
        text = request.form.get("text")
        file = request.files['image']

        if request.files['image']:
            file = request.files['image']
            image_name = save_image(file)
        else:
            image_name = "foto_null_.png"

        db.execute("INSERT INTO news (users_id, header, text, image) VALUES (?, ?, ?, ?)",
                   session["user_id"], header, text, image_name)

        flash('Your news has been added!', 'info')
        return redirect("/")
    else:
        return render_template("add_news.html")

# To view the news in its entirety
@app.route("/show_news")
def show_news():
    id = request.args.get("id")
    news = db.execute("SELECT news.id, users_id, datetime, username, header, image, text FROM news JOIN users ON users.id = news.users_id WHERE news.id = ?", id)
    if len(news) > 0:
        news1 = news[0]
    else:
        return render_template("pardon.html")

    image_path = url_for('static', filename=news1["image"])

    return render_template("show_news.html", news1=news1, image_path=image_path)

# To edit the news
@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        id = request.form.get("id")
        news = db.execute("SELECT users_id, news.id, image, datetime, username, header, text FROM news JOIN users ON users.id = news.users_id WHERE news.id = ?", id)
        if len(news) > 0:
            news1 = news[0]
        else:
            return render_template("pardon.html")
        image_path = url_for('static', filename=news1["image"])

        if session["user_id"] == news1["users_id"]:
            return render_template("edit.html", news1=news1, image_path=image_path)
        else:
            return render_template("pardon.html")
    else:
        return render_template("login.html")

# To save an image to a folder
def save_image(image_form):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(image_form.filename)
    image_name = random_hex + f_ext
    image_path = os.path.join(app.root_path, "static", image_name)
    image_form.save(image_path)
    return image_name

# To save the changes made to the news in the database
@app.route("/save", methods=["GET", "POST"])
@login_required
def save():
    if request.method == "POST":
        if not request.form.get("header"):
            flash('Must fill in the header field!', 'danger')
            return render_template ("edit.html")
        if not request.form.get("text"):
            flash('Must fill in the text field!', 'danger')
            return render_template ("edit.html")
        header = request.form.get("header")
        text = request.form.get("text")
        id = request.form.get("id")

        db.execute("UPDATE news SET header = ?, text = ? WHERE id = ?", header, text, id)

        if request.files['image']:
            file = request.files['image']
            image_name = save_image(file)
            db.execute("UPDATE news SET image = ? WHERE id = ?", image_name, id)

        flash('Your news has been updated!', 'info')
        return redirect("/")
    else:
        return render_template("login.html")

# To remove news
@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    if request.method == "POST":
        id = request.form.get("id")
        news = db.execute("SELECT users_id, news.id, datetime, username, header, text FROM news JOIN users ON users.id = news.users_id WHERE news.id = ?", id)
        if len(news) > 0:
            news1 = news[0]
        else:
            return render_template("pardon.html")

        if session["user_id"] == news1["users_id"]:
            db.execute("DELETE FROM news WHERE id = ?", id)
            flash('Your news has been removed!', 'info')
            return redirect("/")
    else:
        return render_template("login.html")

# Displays user information in an editable form
@app.route("/my_profile")
@login_required
def my_profile():
    profile = db.execute("SELECT username, date_of_birth, address, phone, email FROM users WHERE id = ?", session["user_id"])
    if len(profile) > 0:
        profile1 = profile[0]
    else:
        return render_template("pardon.html")

    if profile1["address"] != None:
        address = profile1["address"]
    else:
        address = ""

    if profile1["email"] != None:
        email = profile1["email"]
    else:
        email = ""

    if profile1["phone"] != None:
        phone = profile1["phone"]
    else:
        phone = ""
    return render_template("my_profile.html", profile1=profile1, address=address, email=email, phone=phone)

# To save the changes made to the user profile in the database
@app.route("/send", methods=["GET", "POST"])
@login_required
def send():
    if request.method == "POST":
        if not request.form.get("name"):
            flash('Must fill in the name field!', 'danger')
            return redirect("/my_profile")
        usernames = db.execute("SELECT username FROM users")

        id = request.form.get("id")
        name = request.form.get("name")
        email = request.form.get("email")
        address = request.form.get("address")
        phone = request.form.get("phone")
        date_of_birth = request.form.get("date_of_birth")

        if name != session["user_name"]:
            for dictionary in usernames:
                if (dictionary["username"]) == name:
                    flash('This username already exists!', 'danger')
                    return redirect("/my_profile")


        db.execute("UPDATE users SET username = ?, email = ?, address = ?, phone = ?, date_of_birth = ? WHERE id = ?", name, email, address, phone, date_of_birth, id)

        rows = db.execute("SELECT * FROM users WHERE id = ?", request.form.get("id"))
        session["user_name"] = rows[0]["username"]
        flash('Your profile was updated!', 'info')
        return redirect("/")
    return render_template("pardon.html")
