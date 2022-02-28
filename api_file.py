"""youtubemusicapi functions and email reminders"""

from ytmusicapi import YTMusic
from time import sleep
from threading import Thread
import smtplib, ssl
import os

from model import User, Artist, Follows, connect_to_db, db
# from env.password.strings import tf_test_development

tf_test_development = os.environ["TF_TEST_DEVELOPMENT"]

headers_auth = os.environ["HEADERS_AUTH_JSON"]

# Authenticates and initializes the YouTube Music API
ytmusic = YTMusic(headers_auth)


# Get artist name and channel id and check if they are in the database, if not it will add them
def search_artist(search_term):
    """Search artist on Youtube music, get search results in list"""

    return ytmusic.search(search_term, filter='artists', limit=1)


def parse_name_id(results):
        """Parse artist name and ID out from search results"""

        # Split search results from artist search
        split_search_results = results.split(",")

        # Get lines that artist name and ID are on 
        artist_name_line = split_search_results[2]
        artist_id_line = split_search_results[5]

        # Gets artist name and ID from their lines 
        artist_name_split = artist_name_line.split(":")
        artist_id_split = artist_id_line.split(":")

        # Instantiates artist name and ID values, and removes quotation marks around values
        artist_name = artist_name_split[1].strip("'")[2:]
        artist_id = artist_id_split[1].strip("'")[2:]

        return artist_name, artist_id


def latest_song(artist):
        """Search for an artists most previous release and parse out the title"""

        # Separate artist name and ID from input
        artist_parsed = artist.split(",")[0][2:-1]

        # Search youtube music for "Artist" latest song
        search_result = ytmusic.search(f"{artist_parsed} latest song", limit=1)

        # Split search result
        split = str(search_result).split(",")

        # Get line that video title is on
        title_line = split[2]

        # Parse for song title
        title = title_line.split(":")[1]

        return title


def check_db(artist_name):
        """Check if the artist is in the database, if not it will search them on Youtube and add them"""

        # Sort through database for matching artist name
        artist_db_name = Artist.query.filter_by(artist_name=artist_name).first()

        if artist_db_name == None:
                print("No artist found, searching youtube")
                search = search_artist(str(artist_name))
                parse = parse_name_id(str(search))
                latest = latest_song(str(parse))

                print(parse)

                new_artist = Artist(artist_name=parse[0], artist_youtube_id=parse[1], artist_previous_song=latest)

                db.session.add(new_artist)
                db.session.commit()

                return new_artist.artist_id
        else:
                return artist_db_name.artist_id


def user_follow_artist(artist_id, user_id):
                

                new_following = Follows( artist_id=artist_id, user_id=user_id)

                db.session.add(new_following)
                db.session.commit()


# Check every half hour for alterations, generate reminder if there are any and send to any user whom follows that artist id in the database

# Loop over database, search each artist, search their latest song, and then compare the value to the latest song in the database, and save all the artists whose latest song has changed to a list. After saving the artist, updates the artists latest song
def check_for_updates():
        artists_list = Artist.query.all()

        updated_artists = []

        for artist in artists_list:
                search = ytmusic.search(artist.artist_name)

                parse_search = parse_name_id(str(search))

                check_update = latest_song(str(parse_search))

                latest_in_db = artist.artist_previous_song

                if check_update != latest_in_db:
                        updated_artists.append(artist.artist_name)

                        artist.artist_previous_song = check_update

                        db.session.commit()

        return updated_artists

# Loop over database and find any users that follow any artist that had a change, then generate an email and send it to that user 
def send_new_song_email(updated_artists):
        
        for artist in updated_artists:
                print(artist)
                artist_obj = Artist.query.filter_by(artist_name=artist).first()
                artist_id = artist_obj.artist_id
                artist_name = artist_obj.artist_name
                song_name = artist_obj.artist_previous_song

                get_followers = Follows.query.filter_by(artist_id=artist_id)

                for follower in get_followers:
                        user_id = follower.user_id
                        get_user = User.query.filter_by(user_id=user_id).first()
                        user_email = get_user.email

                        def email(user_email):
                                port = 465  # For SSL
                                smtp_server = "smtp.gmail.com"
                                sender_email = "tf.test.development@gmail.com"  # My address
                                receiver_email = user_email  # Receiver address
                                password = tf_test_development
                                message = f"\
                                Subject: Hi there\n\n This message is sent from Stalk Star. One of your favorite artists, {artist_name} has a new song called {song_name}!"

                                context = ssl.create_default_context()
                                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                                        server.login(sender_email, password)
                                        server.sendmail(sender_email, receiver_email, message)

                        email(user_email)



if __name__ == "__main__":
        # connect_to_db(app)

        # V V V test functions V V V
        # artist = search_artist("Jack Harlow")
        # parse = parse_name_id(str(artist))
        # latest = latest_song(str(parse))
        # print(latest)

        # while True: 
        #         sleep(1800)
        #         Thread(target = fun).start()

        print(ytmusic.search("jed1-8QSeCc"))
