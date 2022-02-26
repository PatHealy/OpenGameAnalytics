# Developed by Pat Healy
# patwhealy.com

from flask import Flask, request, render_template, abort, get_flashed_messages, flash, session, redirect, send_file
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import pandas as pd

from src.api import UserAPI, UserInfoAPI, SessionAPI, SessionUserAPI, SessionContinueAPI, SessionEndAPI, ActionAPI, IndependentAPI, DependentAPI
from src.models import User, UserInfo, PlaySession, PlaySessionStart, PlaySessionContinue, PlaySessionEnd, PlayAction, IndependentPoint, DependentPoint

from config import admins, database_url, secret_key

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
# API Endpoints
#####################################################

api.add_resource(UserAPI, '/user/<int:game_id>')
api.add_resource(UserInfoAPI, '/user/info')
api.add_resource(SessionAPI, '/session/<int:game_id>')
api.add_resource(SessionUserAPI, '/session/user')
api.add_resource(SessionContinueAPI, '/session/continue')
api.add_resource(SessionEndAPI, '/session/end')
api.add_resource(ActionAPI, '/session/action')
api.add_resource(IndependentAPI, '/experiment/independent')
api.add_resource(DependentAPI, '/experiment/dependent')

#####################################################
# Admin Login
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
	users = pd.read_sql(User.query.statement, User.query.session.bind)
	user_infos = pd.read_sql(UserInfo.query.statement, UserInfo.query.session.bind)
	play_sessions = pd.read_sql(PlaySession.query.statement, PlaySession.query.session.bind)
	play_session_starts = pd.read_sql(PlaySessionStart.query.statement, PlaySessionStart.query.session.bind)
	play_session_continues = pd.read_sql(PlaySessionContinue.query.statement, PlaySessionContinue.query.session.bind)
	play_session_ends = pd.read_sql(PlaySessionEnd.query.statement, PlaySessionEnd.query.session.bind)
	play_actions = pd.read_sql(PlayAction.query.statement, PlayAction.query.session.bind)
	independent_points = pd.read_sql(IndependentPoint.query.statement, IndependentPoint.query.session.bind)
	dependent_points = pd.read_sql(DependentPoint.query.statement, DependentPoint.query.session.bind)

	with pd.ExcelWriter('data_dump.xlsx') as writer:
		users.to_excel(writer, sheet_name="Users")
		user_infos.to_excel(writer, sheet_name="User Infos")
		play_sessions.to_excel(writer, sheet_name="Play Sessions")
		play_session_starts.to_excel(writer, sheet_name="Play Session Starts")
		play_session_continues.to_excel(writer, sheet_name="Play Session Continues")
		play_session_ends.to_excel(writer, sheet_name="Play Session Ends")
		play_actions.to_excel(writer, sheet_name="Play Actions")
		independent_points.to_excel(writer, sheet_name="Independent Points")
		dependent_points.to_excel(writer, sheet_name="Dependent Points")
	return send_file('data_dump.xlsx')

if __name__ == "__main__":
	app.run()