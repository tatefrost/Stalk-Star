from ytmusicapi import YTMusic

from model import User, Artist, Follows, connect_to_db, db

# Authenticates and initializes the YouTube Music API
ytmusic = YTMusic("headers_auth.json")


# Get artist name and channel id and check if they are in the database, if not it will add them

def search_artist(search_term):
    ytmusic.search(search_term)


def parse_name_id(artist):
    pass


def check_db(id):
    pass

# Check every half hour for alterations, generate reminder if there are any and send to any user whom follows that artist id in the database 




if __name__ == "__main__":


    # V V V test functions V V V
    search_artist = ytmusic.search("Billie Eillish")
    search_results = ytmusic.get_artist('UCERrDZ8oN0U_n9MphMKERcg')
    post = ytmusic.get_artist_albums('UCeLHszkByNZtPKcaVXOCOQQ','6gPaAUNxQUJDb0FCQ25FQUFHVnVBQUZWVXdBQlZWTUFBUUJHUlcxMWMybGpYMlJsZEdGcGJGOWhjblJwYzNRQUFRQUJRd0FBQVFBQkFBQUJBUVFCb2xYSUNMd0RHaGhWUTNsRU0xaFhVa3M1YTI4dGFYcG1NbTVDVTBacGRIZUNBUmhWUTNsRU0xaFhVa3M1YTI4dGFYcG1NbTVDVTBacGRIY0FBUkMtMHFXXzA0TDJBaG9DY0drWUFDb1BZWEowYVhOMFgzSmxiR1ZoYzJWek1MSFUwT1dYOGNueWNB')
    albums = ytmusic.get_artist_albums('UCERrDZ8oN0U_n9MphMKERcg', '6gPaAUNxQUJDb0FCQ25FQUFHVnVBQUZWVXdBQlZWTUFBUUJHUlcxMWMybGpYMlJsZEdGcGJGOWhjblJwYzNRQUFRQUJRd0FBQVFBQkFBQUJBUVFCb2xwNkNMd0RHaGhWUTBWU2NrUmFPRzlPTUZWZmJqbE5jR2hOUzBWU1kyZUNBUmhWUTBWU2NrUmFPRzlPTUZWZmJqbE5jR2hOUzBWU1kyY0FBUkNxNFktTDRJVDJBaG9DY0drWUFDb1BZWEowYVhOMFgzSmxiR1ZoYzJWek1MSFUwT1dYOGNueWNB')

    print(post)