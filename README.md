# Stalk-Star
Stalk-Star is a user friendly web application that was created with Python and Flask to allow users to effortlessly keep track of when their favorite artists release a new track. Users have the ability to sign up for Stalk-Star, sign in to Stalk-Star, sign out of Stalk-Star, and search any artist to follow or unfollow. When an artists that is followed by the user releases new content the user will receive an auto generated reminder email to notify the user that the artist has created a new song.

This app was created utilizing Python for the interactivity, Flask for server functionality, HTML5 and CSS for client end fulfillment, werkzeug for password hashing(rest assured, all of your super secret password are safe from me!), and WTForums/ Jinja for exchanging data to and from the back end and the client side. It also makes great use of the YTMusicAPI to search the youtube music library for information in real time, to allow information to be held about the artists in the database which is currently being hosted on Heroku. The artists latest songs are looped over periodically and compared to what is stored in the database, if it is not a match, all users who follow the artist are sent an email notifications to alert them one of their artists has a new song waiting, and then the database updates to reflect the correct most recent track.

![Stalk-Star-image](https://github.com/tatefrost/img-stalk-star/blob/main/Screen%20Shot%202022-02-27%20at%202.57.25%20PM.png?raw=true)

## Technologies used
* Python

* HTML5

* CSS

* Flask

* SQLAlchemy

* YTMusicAPI


## Author
Tate Frost, software engineer located in Salt Lake City, Utah. 
