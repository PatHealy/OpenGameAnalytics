import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_all_user_codes():
	user_infos = pd.read_sql("select * from user_info where attribute_name='study_id' group by info, fk_user_id order by uploaded_at desc;", db.session.bind)
	user_infos = user_infos[user_infos["attribute_name"] == "study_id"]

	user_infos = user_infos[["info", "created_at", "uploaded_at", "fk_user_id"]]
	user_infos = user_infos.rename({"info":"study_id", "fk_user_id":"user_id"})

	table_label = "Users by study_id (only includes users with study_id assigned)"
	table_header = ["study_id", "created_at", "uploaded_at", "user_id"]
	table_data = [[row["study_id"], row["created_at"], row["uploaded_at"], row["user_id"]] for index, row in user_infos.iterrows()]

	return table_label, table_header, table_data