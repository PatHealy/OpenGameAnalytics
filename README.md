## What is OpenGameAnalytics

OpenGameAnalytics is an open-source tool built for video game researchers to keep track of valuable data on player behavior. 

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

### Running the Flask Server

### Connecting a Unity Client


