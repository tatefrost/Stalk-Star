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
def signup_submit():
        """Submit sign up for Stalk-Star account forum"""

        user_name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        password_repeat = request.form["pass2"]

        user_is_in_db = User.query.filter_by(email=email).first()

        if password == password_repeat and not user_is_in_db:
                new_user = User(user_name=user_name, email=email, password=password)

                db.session.add(new_user)
                db.session.commit()

                flash(f"User {email} added")
                return redirect("/signin")
        elif password != password_repeat and user_is_in_db:
                flash("Passwords did not match or email is already registered")
                return redirect("/signup")
    

@app.route('/signin', methods=["GET"])
def signin():
        """Sign into user Stalk-Star page forum"""

        return render_template("signin.html")


@app.route('/signin', methods=["POST"])
def signin_submit():
        """Submit sign into user Stalk-Star page forum"""
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("No user with that email found")
            return redirect("/login")

        if user.password != password:
            flash("Incorrect password")
            return redirect("/login")

        session["user_id"] = user.user_id

        flash("Logged in")
        return redirect(f"/users/{user.user_id}")


@app.route("/signout")
def signout():
        """Log out user"""

        del session["user_id"]
        flash("You are logged out.")
        return redirect("/")

@app.route('/home')
def home():
        """Users Home page for Stalk-Star"""

        return render_template("homepage.html")


@app.route('/artists', methods=["GET"])
def artists():
        """View all artists user follows"""

        return render_template("artists.html")


@app.route('/add-artist', methods=["GET"])
def add_artist():
        """Follow new artists page form"""

        return render_template("add-artist.html")


@app.route('/add-artist', methods=["POST"])
def add_artist_submit():
        """Submit follow new artists page form"""

        return redirect("/artists")


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
