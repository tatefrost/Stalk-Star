"""Models and database functions for Stalk-Star"""

import os
import requests

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint

db_uri = os.environ["DB_URI"]

db = SQLAlchemy()


class User(db.Model):
    """User of Stalk-Star website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"


class Artist(db.Model):
    """An artist on Youtube"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(64), nullable=False)
    artist_youtube_id = db.Column(db.String(), nullable=True)
    artist_previous_song = db.Column(db.String(200), nullable=True)

    def __repr__(self):

        return f"<Artist artist_id={self.artist_id} name={self.artist_name} artist_youtube_id ={self.artist_youtube_id} previous_song={self.artist_previous_song}>"


class Follows(db.Model):
    """A user to artist following relationship"""

    __tablename__ = "artist_followers"

    following_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))

    user = db.relationship("User", backref=db.backref("stalk-star", order_by=artist_id))

    artist = db.relationship("Artist", backref=db.backref("stalk-star", order_by=artist_id))

    def __repr__(self):

        return f"<followings following_id={self.following_id} user_id={self.user_id} artist_id={self.artist_id}>"


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'{db_uri}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print("Connected to DB.")