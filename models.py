from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
	pk_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String)
	token = db.Column(db.String)
	game_name = db.Column(db.String)

class UserInfo(db.Model):
	pk_user_info_id = db.Column(db.Integer, primary_key=True)
	attribute_name = db.Column(db.String)
	info = db.Column(db.Text)
	created_at = db.Column(db.DateTime)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.pk_user_id'))

class PlaySession(db.Model):
	pk_play_session_id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.pk_user_id'))

class PlaySessionContinue(db.Model):
	pk_play_session_continue_id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime)
	fk_play_session_id = db.Column(db.Integer, db.ForeignKey('play_session.pk_play_session_id'))

class PlaySessionEnd(db.Model):
	pk_play_session_end_id = db.Column(db.Integer, primary_key=True)
	created_at = db.Column(db.DateTime)
	fk_play_session_id = db.Column(db.Integer, db.ForeignKey('play_session.pk_play_session_id'))

class PlayAction(db.Model):
	pk_play_action_id = db.Column(db.Integer, primary_key=True)
	action_name = db.Column(db.String)
	info = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.pk_user_id'))
	fk_play_session_id = db.Column(db.Integer, db.ForeignKey('play_session.pk_play_session_id'))

class IndependentPoint(db.Model):
	pk_independent_point_id = db.Column(db.Integer, primary_key=True)
	attribute_name = db.Column(db.String)
	info = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.pk_user_id'))

class DependentPoint(db.Model):
	pk_dependent_point_id = db.Column(db.Integer, primary_key=True)
	attribute_name = db.Column(db.String)
	info = db.Column(db.String)
	created_at = db.Column(db.DateTime)
	fk_user_id = db.Column(db.Integer, db.ForeignKey('user.pk_user_id'))
