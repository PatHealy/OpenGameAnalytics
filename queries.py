import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_all_user_codes():
	user_infos = pd.read_sql("select info as study_id, created_at, uploaded_at, fk_user_id as user_id from user_info where attribute_name='study_id' group by info, fk_user_id order by uploaded_at desc;", db.session.bind)
	table_label = "Users by study_id (only includes users with study_id assigned)"
	table_header = ["study_id", "created_at", "uploaded_at", "user_id"]
	table_data = [[row["study_id"], row["created_at"], row["uploaded_at"], row["user_id"]] for index, row in user_infos.iterrows()]

	return table_label, table_header, table_data