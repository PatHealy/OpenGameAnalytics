## What is OpenGameAnalytics

OpenGameAnalytics is an open-source tool built for video game researchers to keep track of data on player behavior. 

It consists of a Flask server back-end connected to a MySQL database and Unity client package. The Flask server hosts a fully REST-ful API, so one could easily develop a new client package to access the API from another game engine or software.

In order to use OpenGameAnalytics, you must host the Flask server and SQL database yourself and simply add the client package to your game. Please refer to the Quick Start Guide below.

## What data is OpenGameAnalytics built to support?

Our database is constructed specifically to serve the needs of serious games researchers, but these needs could be expanded with small modifications.

The application is built to collect:
- Users identified by randomly generated tokens per device
- Session data regarding the start, end, and duration of a player's play session
- Player actions during a play session
- Conditions assigned to the player for the purposes of experimentation (i.e. independent variables)
- Data capturing study endpoints (i.e. dependent variables)
- Information about the player that we don't expect to change during play (i.e. demographics)

You can find the structure of this database in [the API documentation](https://docs.google.com/document/d/1boJc0PTgcztlJy4J4IM-3FxQNMzzfH5-iXgfxh5r_A4/edit?usp=sharing).

## Quick Start Guide

To get started, you need to get the Flask server running and set a client up to connect to it.

### Running the Flask Server

The entire Flask server runs off of two files: `app.py` and `models.py`. 

For the Flask server to run properly, you'll need your database hosted somewhere. I run my own deployment of OpenGameAnalytics with a MySQL server but in theory you can use any SQL-style relational database with some modification. By default, as you can see in the `app.py` source code, the application will connect to the SQLite database at `test.db`. See the source code below that begins around line 20:

```python
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
# 	username="XXXXXXXXXXXXXXXX",
# 	password="XXXXXXXXXXXXX",
# 	hostname="XXXXXXXXXXXXXXX",
# 	databasename="XXXXXXXXXXX",
# )

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
```
For testing purposes, go ahead and try the following steps with the code unchanged! The code will run fine with the SQLite database connection but this is not recommended if you expect a large number of users. 

To connect to your own MySQL server, simply modify the database credentials in lines 21-24 per your database, uncomment lines 20-25, and remove the SQLite line at line 27. The schema for the database is found in `schema.sql`.

There is one other line you will definitely need to edit! See line 44 below:

```python
game_dictionary = {959742: "Example Game"}
```

This game dictionary details the games this instance of OpenGameAnalytics will keep track of. This allows you to use one instance of the server to collect data for a whole bunch of games! The keys in this dictionary are referred to elsewhere as `GAME_ID` for the given game and the values are the names of the games. So, this dictionary defines that this instance of the server will support one game, named "Example Game" with `GAME_ID` of 959742. Modify this line to instead track your own game (or games) -- the `GAME_ID` should be a 6-digit integer.

#### Running Flask Locally

To run the Flask server locally (which you should totally do to test your game), jump into a terminal and cd over to the project directory. Assuming you have the Python packages listed in `requirements.txt` installed (I'd recommend doing that in a Virtual Environment!), you can run the server with the following two lines:

```bash
export FLASK_APP=app.py
flask run
```

*Note*: If you're on Windows, you need to use `set` instead of `export`.

#### Deploying Flask

If you want deploy the Flask server so you can use it *in the wild*, there are a number of services you can use to easily get up-and-running. Here are some options:

- The easiest is probably [Python Anywhere](https://help.pythonanywhere.com/pages/Flask/), which also gives you a MySQL database for pretty cheap.
- Here are a bunch of deployment options from [Flask itself](https://flask.palletsprojects.com/en/2.0.x/deploying/index.html)

### Connecting a Unity Client















