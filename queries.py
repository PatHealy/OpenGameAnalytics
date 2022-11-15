import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_user_link(user_id):
	return """<a href="/admin/dashboard/user/""" + str(user_id) + """">""" + str(user_id) + "</a>"

def get_session_link(session_id):
	return """<a href="/admin/dashboard/session/""" + str(session_id) + """">""" + str(session_id) + "</a>"

def get_all_user_codes():
	user_infos = pd.read_sql("select info as study_id, created_at, uploaded_at, fk_user_id as user_id from user_info where attribute_name='study_id' group by info, fk_user_id order by uploaded_at desc;", db.session.bind)
	table_label = "Users with study_id's"
	table_description = "<p>All of the study_id's logged in the database.</p><p>If a user has logged the same study_id multiple times, this shows the first time it was logged</p><p>Click on the user_id to see a detailed summary of the user's activity</p>"
	table_header = ["study_id", "created_at", "uploaded_at", "user_id"]
	table_data = [[row["study_id"], row["created_at"], row["uploaded_at"], get_user_link(row["user_id"])] for index, row in user_infos.iterrows()]

	return table_label, table_description, table_header, table_data

def get_user_sessions(user_id):
	sessions_info = pd.read_sql("""
			select pk_play_session_id as play_session_id, play_session.created_at as start_time, max(play_session_continue.created_at) as end_time, TIMEDIFF(max(play_session_continue.created_at), play_session.created_at) as session_length 
			from play_session join play_session_continue on pk_play_session_id=fk_play_session_id
			where fk_user_id = %(user_id)s group by pk_play_session_id
			order by pk_play_session_id desc;
		""",
	    db.session.bind,
	    params={"user_id":user_id}
	)

	table_label = "Sessions of user #" + str(user_id)
	table_description = ""
	table_header = ["play_session_id", "start_time", "end_time", "session_length"]
	table_data = [[get_session_link(row["play_session_id"]), row["start_time"], row["end_time"], row["session_length"]] for index, row in sessions_info.iterrows()]

	return table_label, table_description, table_header, table_data