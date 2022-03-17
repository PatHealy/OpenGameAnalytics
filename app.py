# Developed by Pat Healy
# patwhealy.com

from flask import Flask, request, render_template, abort, get_flashed_messages, flash, session, redirect, send_file, jsonify, Response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from http import HTTPStatus
import pandas as pd
import random
import string
from dateutil import parser

from models import User, UserInfo, PlaySession, PlaySessionContinue, PlaySessionEnd, PlayAction, IndependentPoint, DependentPoint
from config import admins, database_url, secret_key, game_dictionary

#####################################################
# Initialization
#####################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

app.secret_key = secret_key

#####################################################
# Helper functions
#####################################################
def username_ganerator(size=30, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def auth(un, tk):
	return check_password_hash(User.query.filter_by(username=un).first().token, tk)

#####################################################
# RESTful API Endpoints
#####################################################

# /user
class UserAPI(Resource):
	def get(self, game_id):
		if game_id in game_dictionary.keys():
			username = username_ganerator()
			token_plain = username_ganerator(size=50)
			user = {'username': username, 'token': token_plain}
			token = generate_password_hash(token_plain, method='pbkdf2:sha256', salt_length=8)
			new_user = User(username=username, token=token, game_name=game_dictionary[game_id])
			db.session.add(new_user)
			db.session.commit()
			res = jsonify(user)
			# res.status = HTTPStatus.CREATED
			return res
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# def post(self):
# 	pass

# /user/info
class UserInfoAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		user_info = json_data['data_point']

		if auth(user['username'], user['token']):
			new_info = UserInfo(attribute_name=user_info['attribute_name'], info=user_info['info'], created_at=parser.parse(json_data['created_at']),
			                    fk_user_id=User.query.filter_by(username=user['username']).first().pk_user_id)
			db.session.add(new_info)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)

# /session
class SessionAPI(Resource):
	def post(self, game_id):
		json_data = request.get_json(force=True)
		user = json_data['user']
		if game_id in game_dictionary.keys() and auth(user['username'], user['token']):
			new_ses = PlaySession(created_at=parser.parse(json_data['created_at']), fk_user_id=User.query.filter_by(username=user['username']).first().pk_user_id)
			db.session.add(new_ses)
			res = jsonify({'play_session_id': new_ses.pk_play_session_id})
			db.session.commit()
			return res
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# /session/continue
class SessionContinueAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']

		if auth(user['username'], user['token']):
			new_ses_continue = PlaySessionContinue(fk_play_session_id=play_session_id, created_at=parser.parse(json_data['created_at']))
			db.session.add(new_ses_continue)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# /session/end
class SessionEndAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']

		if auth(user['username'], user['token']):
			new_ses_end = PlaySessionEnd(fk_play_session_id=play_session_id, created_at=parser.parse(json_data['created_at']))
			db.session.add(new_ses_end)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)

# /session/action
class ActionAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']
		action = json_data['data_point']

		if auth(user['username'], user['token']):
			new_action = PlayAction(action_name=action['attribute_name'], info=action['info'], created_at=parser.parse(json_data['created_at']),
			                        fk_user_id=User.query.filter_by(username=user['username']).first().pk_user_id,
			                        fk_play_session_id=play_session_id)
			db.session.add(new_action)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# /experiment/independent
class IndependentAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		point_data = json_data['data_point']

		if auth(user['username'], user['token']):
			new_point = IndependentPoint(attribute_name=point_data['attribute_name'], info=point_data['info'], created_at=parser.parse(json_data['created_at']),
			                             fk_user_id=User.query.filter_by(username=user['username']).first().pk_user_id)
			db.session.add(new_point)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# /experiment/dependent
class DependentAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		point_data = json_data['data_point']

		if auth(user['username'], user['token']):
			new_point = DependentPoint(attribute_name=point_data['attribute_name'], info=point_data['info'], created_at=parser.parse(json_data['created_at']),
			                           fk_user_id=User.query.filter_by(username=user['username']).first().pk_user_id)
			db.session.add(new_point)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)

api.add_resource(UserAPI, '/user/<int:game_id>')
api.add_resource(UserInfoAPI, '/user/info')
api.add_resource(SessionAPI, '/session/<int:game_id>')
api.add_resource(SessionContinueAPI, '/session/continue')
api.add_resource(SessionEndAPI, '/session/end')
api.add_resource(ActionAPI, '/session/action')
api.add_resource(IndependentAPI, '/experiment/independent')
api.add_resource(DependentAPI, '/experiment/dependent')

#####################################################
# Admin Dashboard
#####################################################

@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
	if request.method == "GET":
		return render_template("admin_login.html", messages=get_flashed_messages())
	elif request.method == "POST":
		if request.form["username"] in admins.keys():
			if admins[request.form["username"]] == request.form["password"]:
				session["username"] = request.form["username"]
				session["password"] = request.form["password"]
				flash("Log in successful.")
				return redirect("/admin/dashboard")
		return abort(404)
	else:
		return abort(404)

@app.route("/admin/dashboard")
def admin_dashboard():
	if admins[session["username"]] == session["password"]:
		return render_template("admin_dashboard.html", messages=get_flashed_messages())
	return abort(404)

@app.route("/admin/dump")
def download_contents():
	users = pd.read_sql("select * from user;", db.session.bind)
	user_infos = pd.read_sql("select * from user_info;", db.session.bind)
	play_sessions = pd.read_sql("select * from play_session;", db.session.bind)
	play_session_continues = pd.read_sql("select * from play_session_continue;", db.session.bind)
	play_session_ends = pd.read_sql("select * from play_session_end;", db.session.bind)
	play_actions = pd.read_sql("select * from play_action;", db.session.bind)
	independent_points = pd.read_sql("select * from independent_point;", db.session.bind)
	dependent_points = pd.read_sql("select * from dependent_point;", db.session.bind)

	with pd.ExcelWriter('data_dump.xlsx') as writer:
		users.to_excel(writer, sheet_name="Users")
		user_infos.to_excel(writer, sheet_name="User Infos")
		play_sessions.to_excel(writer, sheet_name="Play Sessions")
		play_session_continues.to_excel(writer, sheet_name="Play Session Continues")
		play_session_ends.to_excel(writer, sheet_name="Play Session Ends")
		play_actions.to_excel(writer, sheet_name="Play Actions")
		independent_points.to_excel(writer, sheet_name="Independent Points")
		dependent_points.to_excel(writer, sheet_name="Dependent Points")
	return send_file('data_dump.xlsx')

if __name__ == "__main__":
	app.run()