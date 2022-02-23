"""Stalk-Star Server"""

from sqlite3 import connect
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Artist, Follows, connect_to_db, db

import api_file as ytapi

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

        email = request.form["email"]
        password = request.form["password"]
        password_repeat = request.form["pass2"]

        user_is_in_db = User.query.filter_by(email=email).first()

        if password == password_repeat and not user_is_in_db:
                new_user = User(email=email, password=password)

                db.session.add(new_user)
                db.session.commit()

                flash(f"User {email} added")
                return redirect("/signin")
        elif password != password_repeat or user_is_in_db:
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
            return redirect("/signin")

        if user.password != password:
            flash("Incorrect password")
            return redirect("/signin")

        session["user_id"] = user.user_id

        flash("Logged in")
        return redirect(f"/home/{user.user_id}")


@app.route("/signout")
def signout():
        """Log out user"""

        del session["user_id"]
        flash("You are logged out.")
        return redirect("/")

@app.route('/home/<int:user_id>', methods=["GET"])
def home(user_id):
        """Users Home page for Stalk-Star"""

        user = User.query.get(user_id)

        return render_template("homepage.html", user=user)


@app.route('/artists/<int:user_id>', methods=["GET"])
def artists(user_id):
        """View all artists user follows"""

        ytapi.send_new_song_email(ytapi.check_for_updates())

        user = User.query.get(user_id)
        artists_id_list = Follows.query.filter_by(user_id=user_id)

        artist_names = []

        for artist in artists_id_list:
                artist_object = Artist.query.filter_by(artist_id=artist.artist_id).first()

                if artist_object != None:
                        name = artist_object.artist_name

                        artist_names.append(name)

        return render_template("artists.html", artists_list=artist_names, user=user)


@app.route('/artists-filter/<int:user_id>', methods=["POST"])
def search_artists(user_id):
        """Search through all artists a user follows"""

        user = User.query.get(user_id)
        search = request.form["filter"]

        if search != "":
                check_db_for_artist = ytapi.check_db(search)
                artists_list = Follows.query.filter_by(user_id=user.user_id, artist_id=check_db_for_artist).first()
                get_artist = Artist.query.filter_by(artist_id=artists_list.artist_id).first()
                artist_name = [get_artist.artist_name]

                return render_template("artists.html", artists_list=artist_name, user=user)
        else:
                return redirect(f"/artists/{user_id}")


@app.route('/artists-delete/<artist>', methods=["POST"])
def delete_artist(artist):
        """Unfollow an artist that a user follows"""

        user_id = session.get("user_id")

        get_artist = Artist.query.filter_by(artist_name=artist).first()

        get_following = Follows.query.filter_by(user_id=user_id, artist_id=get_artist.artist_id).first()

        db.session.delete(get_following)
        db.session.commit()

        return redirect(f"/artists/{user_id}")


@app.route('/add-artist/<int:user_id>', methods=["GET"])
def add_artist(user_id):
        """Follow new artists page form"""

        user = User.query.get(user_id)

        return render_template("add-artist.html", user=user)


@app.route('/add-artist/<int:user_id>', methods=["POST"])
def add_artist_submit(user_id):
        """Submit follow new artists page form"""

        search = request.form["search"]

        artist_search_result = ytapi.search_artist(str(search))

        artist_parsed = ytapi.parse_name_id(str(artist_search_result))

        artist_name = artist_parsed[0]

        check_db_for_artist = ytapi.check_db(artist_name)

        does_user_follow = Follows.query.filter_by(artist_id=check_db_for_artist).first()

        if does_user_follow:
                flash("You already follow that artist!")
        else:  
                ytapi.user_follow_artist(check_db_for_artist, user_id)

        return redirect(f"/artists/{user_id}")


@app.route('/about')
def about():
        """Information about Stalk-Star"""

        return render_template("about.html")


if __name__ == "__main__":
        # Must set debug=True for when DebugToolbarExtension is invoked 
        app.debug = True

        app.jinja_env.auto_reload = app.debug
        
        # Turns off developer intercept on page redirects
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

        connect_to_db(app)

        # assure templates, etc. are not cached in debug mode
        DebugToolbarExtension(app)

        app.run(port=5000, host='0.0.0.0')
