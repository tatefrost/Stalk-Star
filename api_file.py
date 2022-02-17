from ytmusicapi import YTMusic
from time import sleep
from threading import Thread

from model import User, Artist, Follows, connect_to_db, db

# Authenticates and initializes the YouTube Music API
ytmusic = YTMusic("headers_auth.json")


# Get artist name and channel id and check if they are in the database, if not it will add them
def search_artist(search_term):
    """Search artist on Youtube music, get search results in list"""

    return ytmusic.search(search_term, filter='artists', limit=2)


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
        artist_parsed = artist.split(",")[0][1:]

        # Search youtube music for "Artist" latest song
        search_result = ytmusic.search(f"{artist_parsed} latest song")

        # Split search result
        split = str(search_result).split(",")

        # Get line that video title is on
        title_line = split[2]

        # Parse for song title
        title = title_line.split(":")[1][1:]

        return title


def check_db(artist_name):
        """Check if the artist is in the database, if not it will search them on Youtube and add them"""

        # Sort through database for matching artist name
        artist_db_name = Artist.query.filter_by(artist_name=artist_name).first()

        if not artist_db_name:
                print("No artist found, searching youtube")
                search = search_artist(str(artist_name))
                parse = parse_name_id(str(search))
                latest = latest_song(str(parse))

                new_artist = Artist(artist_name=parse[0][1:], artist_youtube_id=parse[1][1:], artist_previous_song=latest)

                db.session.add(new_artist)
                db.session.commit()



# Check every half hour for alterations, generate reminder if there are any and send to any user whom follows that artist id in the database

# Loop over database, search each artist, search their latest song, and then compare the value to the latest song in the database, and save all the artists whose latest song has changed
def check_for_updates():
        pass

# Loop over database and find any users that follow any artist that had a change, then generate an email and send it to that user 
def send_new_song_email():
        pass

# change artists lastest songs to new song that have changed
def update_database_latest_songs():
        pass


if __name__ == "__main__":
        # connect_to_db(app)

        # V V V test functions V V V
        artist = search_artist("Drake")
        parse = parse_name_id(str(artist))
        latest = latest_song(str(parse))
        print(latest)

        # while True:
        #         sleep(1800)
        #         Thread(target = fun).start()

    
