# Developed by Pat Healy
# patwhealy.com
# Last edited 11/1/21

from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

import random
import string

from models import User, User_Info, Play_Session, Play_Session_Start, Play_Session_Continue, Play_Session_End, Play_Action, Independent_Point, Dependent_Point

#####################################################
# Initialization
#####################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
	username="XXXXXXXXXXXXXXXX",
	password="XXXXXXXXXXXXX",
	hostname="XXXXXXXXXXXXXXX",
	databasename="XXXXXXXXXXX",
)
db = SQLAlchemy(app)
api = Api(app)


#####################################################
# Helper functions
#####################################################
def username_ganerator(size=30, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def auth(un, tk):
	return check_password_hash(User.query.filter_by(username=un).first().token, tk)

#####################################################
# RESTful API
#####################################################

#/user
class UserAPI(Resource):
	def get(self):
		username = username_ganerator()
		token_plain = username_ganerator(size=50)
		user = {'username': username, 'token': token_plain}
		token = generate_password_hash(token_plain, method='pbkdf2:sha256', salt_length=8)
		new_user = User(username=username, token=token)
		db.session.add(new_user)
		db.session.commit()
		res = jsonify(user)
		res.status = HTTPStatus.CREATED
		return res

	# def post(self):
	# 	pass

#/user/info
class UserInfoAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		user_info = json_data['user_info']

		if auth(user['username'], user['token']):
			new_info = User_Info(attribute_name=user_info['attribute_name'], info=user_info['info'], fk_user_id=User.query.filter_by(username=un).first().pk_user_id)
			db.session.add(new_info)
			db.session.commit()
			return make_response(status=HTTPStatus.CREATED)
		else:
			return make_response(status=HTTPStatus.FORBIDDEN)

#/session
class SessionAPI(Resource):
	def get(self):
		new_ses = Play_Session()
		db.session.add(new_ses)
		db.session.commit()
		res = jsonify({'play_session_id': new_ses.pk_play_session_id})
		res.status = HTTPStatus.CREATED
		return res

#/session/user
class SessionUserAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']

		if auth(user['username'], user['token']):
			play_ses = Play_Session.query.filter_by(pk_play_session_id=play_session_id).first()
			play_ses.fk_user_id = User.query.filter_by(username=un).first().pk_user_id

			new_ses_start = Play_Session_Start(fk_play_session_id=play_session_id)

			db.session.add(new_ses_start)
			db.session.commit()
			return make_response(status=HTTPStatus.CREATED)
		else:
			return make_response(status=HTTPStatus.FORBIDDEN)

#/session/continue
class SessionContinueAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']

		if auth(user['username'], user['token']):
			new_ses_continue = Play_Session_Continue(fk_play_session_id=play_session_id)
			db.session.add(new_ses_continue)
			db.session.commit()
			return make_response(status=HTTPStatus.CREATED)
		else:
			return make_response(status=HTTPStatus.FORBIDDEN)

#/session/end
class SessionEndAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']

		if auth(user['username'], user['token']):
			new_ses_end = Play_Session_End(fk_play_session_id=play_session_id)
			db.session.add(new_ses_end)
			db.session.commit()
			return make_response(status=HTTPStatus.CREATED)
		else:
			return make_response(status=HTTPStatus.FORBIDDEN)

#/session/action
class ActionAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']
		action = json_data['action']

		if auth(user['username'], user['token']):
			new_action = Play_Action(action_name=action['action_name'], info=action['info'], fk_user_id=User.query.filter_by(username=un).first().pk_user_id, fk_play_session_id=play_session_id)
			db.session.add(new_action)
			db.session.commit()
			return make_response(status=HTTPStatus.CREATED)
		else:
			return make_response(status=HTTPStatus.FORBIDDEN)

#/experiment/independent
class IndependentAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		point_data = json_data['independent_point']

		if auth(user['username'], user['token']):
			new_point = Independent_Point(attribute_name=point_data['attribute_name'], info=point_data['info'], fk_user_id=User.query.filter_by(username=un).first().pk_user_id)
			db.session.add(new_point)
			db.session.commit()
			return make_response(status=HTTPStatus.CREATED)
		else:
			return make_response(status=HTTPStatus.FORBIDDEN)

#/experiment/dependent
class DependentAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		point_data = json_data['dependent_point']

		if auth(user['username'], user['token']):
			new_point = Dependent_Point(attribute_name=point_data['attribute_name'], info=point_data['info'], fk_user_id=User.query.filter_by(username=un).first().pk_user_id)
			db.session.add(new_point)
			db.session.commit()
			return make_response(status=HTTPStatus.CREATED)
		else:
			return make_response(status=HTTPStatus.FORBIDDEN)

api.add_resource(UserAPI, '/user')
api.add_resource(UserInfoAPI, '/user/info')
api.add_resource(SessionAPI, '/session')
api.add_resource(SessionUserAPI, '/session/user')
api.add_resource(SessionContinueAPI, '/session/continue')
api.add_resource(SessionEndAPI, '/session/end')
api.add_resource(ActionAPI, '/session/action')
api.add_resource(IndependentAPI, '/experiment/independent')
api.add_resource(DependentAPI, '/experiment/dependent')

