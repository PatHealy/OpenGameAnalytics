from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class UserAPI(Resource):
	def get(self, id):
		pass

	def put(self, id):
		pass

class DataAPI(Resource):
	def put(self, id):
		pass

class ActionAPI(Resource):
	def put(self, id):
		pass

class SessionAPI(Resource):
	def put(self, id):
		pass

api.add_resource(UserAPI, '/user/<int:id>', endpoint = 'user')