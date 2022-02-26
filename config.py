#recommend using a 6-digit number
game_dictionary = {959742: "Example Game"}

#Database URL for SQLite
database_url = "sqlite:///data/test.db"

#Database URL for MySQL
# database_url = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
# 	username="XXXXXXXXXXXXXXXX",
# 	password="XXXXXXXXXXXXX",
# 	hostname="XXXXXXXXXXXXXXX",
# 	databasename="XXXXXXXXXXX",
# )

#The usernames and passwords of admins, who will be able to view the data through the admins portal
#No, this is not very secure
admins = {"admin_name": "admin_password"}

#The secret key for flask sessions
secret_key = "development_key"