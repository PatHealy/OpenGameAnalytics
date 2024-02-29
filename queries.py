import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_user_link(user_id):
	return {"link":"/admin/dashboard/user/""" + str(user_id), "content":user_id}

def get_session_link(session_id):
	return {"link":"/admin/dashboard/session/""" + str(session_id), "content":session_id}

def compile_table_data(label, description, header, data):
	comp = {}
	comp['label'] = label
	comp['description'] = description
	comp['header'] = header
	comp['data'] = data
	return comp

def get_all_user_codes():
	user_infos = pd.read_sql("select info as study_id, created_at, uploaded_at, fk_user_id as user_id from user_info where attribute_name='study_id' and info!='1234' group by info, fk_user_id order by uploaded_at desc;", db.session.bind)
	table_label = "Users with study_id's"
	table_description = "All of the study_id's logged in the database. If a user has logged the same study_id multiple times, this shows the first time it was logged. Click on the user_id to see a detailed summary of the user's activity."
	table_header = ["study_id", "created_at", "uploaded_at", "user_id"]
	table_data = [[row["study_id"], row["created_at"], row["uploaded_at"], get_user_link(row["user_id"])] for index, row in user_infos.iterrows()]

	return compile_table_data(table_label, table_description, table_header, table_data)

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

	return compile_table_data(table_label, table_description, table_header, table_data)



def get_user_conditions(user_id):
	condition_info = pd.read_sql("""
		select attribute_name, info, created_at, uploaded_at from LearningTechLab$GameAnalytics.independent_point where fk_user_id=%(user_id)s;
		""",
	    db.session.bind,
	    params={"user_id":user_id}
	)

	table_label = "Assigned Conditions of user #" + str(user_id)
	table_description = ""
	table_header = ["attribute_name", "info", "created_at", "uploaded_at"]
	table_data = [[row["attribute_name"], row["info"], row["created_at"], row["uploaded_at"]] for index, row in condition_info.iterrows()]

	return compile_table_data(table_label, table_description, table_header, table_data)

def get_session_actions(session_id):
	action_info = pd.read_sql("""
		select action_name, info, created_at, uploaded_at from play_action where fk_play_session_id=%(session_id)s;
		""",
	    db.session.bind,
	    params={"session_id":session_id}
	)

	table_label = "Actions of user during session " + str(session_id)
	table_description = ""
	table_header = ["action_name", "info", "created_at", "uploaded_at"]
	table_data = [[row["action_name"], row["info"], row["created_at"], row["uploaded_at"]] for index, row in condition_info.iterrows()]

	return compile_table_data(table_label, table_description, table_header, table_data)



#select action_name, info, created_at, uploaded_at from play_action where fk_play_session_id=27;