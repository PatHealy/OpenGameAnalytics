
from flask import jsonify, Response, request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from http import HTTPStatus

import random
import string

from src.models import User, UserInfo, PlaySession, PlaySessionStart, PlaySessionContinue, PlaySessionEnd, PlayAction, IndependentPoint, DependentPoint

from config import game_dictionary

#####################################################
# RESTful API
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
			new_info = UserInfo(attribute_name=user_info['attribute_name'], info=user_info['info'],
			                    fk_user_id=User.query.filter_by(username=user['username']).first().pk_user_id)
			db.session.add(new_info)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# /session
class SessionAPI(Resource):
	def get(self, game_id):
		if game_id in game_dictionary.keys():
			new_ses = PlaySession()
			db.session.add(new_ses)
			db.session.commit()
			res = jsonify({'play_session_id': new_ses.pk_play_session_id})
			# res.status = HTTPStatus.CREATED
			return res
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# /session/user
class SessionUserAPI(Resource):
	def post(self):
		json_data = request.json
		user = json_data['user']
		play_session_id = json_data['play_session_id']

		if auth(user['username'], user['token']):
			play_ses = PlaySession.query.filter_by(pk_play_session_id=play_session_id).first()
			play_ses.fk_user_id = User.query.filter_by(username=user['username']).first().pk_user_id
			db.session.merge(play_ses)
			# db.session.commit()
			# db.session.commit()
			db.session.commit()

			# db.session.flush()

			new_ses_start = PlaySessionStart(fk_play_session_id=play_session_id)
			db.session.add(new_ses_start)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)


# /session/continue
class SessionContinueAPI(Resource):
	def post(self):
		json_data = request.get_json(force=True)
		user = json_data['user']
		play_session_id = json_data['play_session_id']

		if auth(user['username'], user['token']):
			new_ses_continue = PlaySessionContinue(fk_play_session_id=play_session_id)
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
			new_ses_end = PlaySessionEnd(fk_play_session_id=play_session_id)
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
			new_action = PlayAction(action_name=action['attribute_name'], info=action['info'],
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
			new_point = IndependentPoint(attribute_name=point_data['attribute_name'], info=point_data['info'],
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
			new_point = DependentPoint(attribute_name=point_data['attribute_name'], info=point_data['info'],
			                           fk_user_id=User.query.filter_by(username=user['username']).first().pk_user_id)
			db.session.add(new_point)
			db.session.commit()
			return Response(status=HTTPStatus.CREATED)
		else:
			return Response(status=HTTPStatus.FORBIDDEN)

#####################################################
# Helper functions
#####################################################
def username_ganerator(size=30, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def auth(un, tk):
	return check_password_hash(User.query.filter_by(username=un).first().token, tk)