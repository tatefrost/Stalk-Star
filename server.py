"""Stalk-Star Server"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Artist, Follows, connect_to_db, db

app = Flask(__name__)

# this is required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Landing page"""

    return render_template("landingpage.html")


@app.route('/signup', methods=['GET'])
def signup():
    """Sign up form for a Stalk-Star account"""

    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signingup():
    """Sign up for Stalk-Star account submit"""

    user_name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(user_name=user_name, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added!")
    return redirect("/home")


@app.route('/signin', methods=["GET"])
def signin():
    """Sign into user Stalk-Star page"""

    return render_template("signin.html")


@app.route('/home')
def home():
    """Home page for Stalk-Star"""

    return render_template("homepage.html")


@app.route('/artists')
def artists():
    """View all artists user follows"""

    return render_template("artists.html")


@app.route('/add-artist')
def add_artist():
    """Follow new artists"""

    return render_template("add-artist.html")


@app.route('/about')
def about():
    """Information about Stalk-Star"""

    return render_template("about.html")


if __name__ == "__main__":
    # Must set debug=True for when DebugToolbarExtension is invoked 
    app.debug = True

    app.jinja_env.auto_reload = app.debug

    # assure templates, etc. are not cached in debug mode
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
