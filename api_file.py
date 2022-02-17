from ytmusicapi import YTMusic

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

        # Search youtube music for "Artist" latest song
        search_result = ytmusic.search(f"{artist} latest song")

        # Split search result
        split = str(search_result).split(",")

        # Get line that video title is on
        title_line = split[2]

        # Parse for song title
        title = title_line.split(":")[1][1:]

        return title


def check_db(id):
        """Check if the artist is in the database"""

    
        pass

# Check every half hour for alterations, generate reminder if there are any and send to any user whom follows that artist id in the database 




if __name__ == "__main__":


        # V V V test functions V V V
        artist = search_artist("Guns n' roses")
        parse = parse_name_id(str(artist))
        latest = latest_song(str(parse).split(",")[0][1:])
        print(latest)
    
