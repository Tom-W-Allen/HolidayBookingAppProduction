from os import path, getenv
from waitress import serve
from flask_wtf.csrf import CSRFProtect

from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager
from dotenv import load_dotenv
import secrets
from domains.user.models.UserSession import UserSession
from domains.user.UserRepository import UserRepository
from mappers.LoginPageMapper import LoginPageMapper
from persistence.CreateSqliteDatabase import set_up_sqlite_database
from persistence.DatabaseFactory import get_database

from blueprints.HomeBlueprint import home_blueprint
from blueprints.RequestBlueprint import request_blueprint
from blueprints.ApproveBlueprint import approve_blueprint
from blueprints.CreateProjectBlueprint import create_project_blueprint
from blueprints.ProjectReviewBlueprint import project_review_blueprint
from blueprints.EditProfileBlueprint import edit_profile_blueprint

# login_manager object set up in accordance with Flask-Login (2024) documentation.
login_manager = LoginManager()
application = Flask(__name__)
application.secret_key = secrets.token_hex()
forgery_protection = CSRFProtect(application)

application.register_blueprint(home_blueprint)
application.register_blueprint(request_blueprint)
application.register_blueprint(approve_blueprint)
application.register_blueprint(create_project_blueprint)
application.register_blueprint(project_review_blueprint)
application.register_blueprint(edit_profile_blueprint)

login_manager.init_app(application)
login_manager.login_view = 'login'

database = get_database(True)

user_repository = UserRepository(database)

login_page_mapper = LoginPageMapper(user_repository)


@login_manager.user_loader
def user_loader(user_id):
    if "logged_in" in session.keys() and str(user_id) in session["logged_in"]:
        return UserSession(user_id)

    return None


@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        page_data = login_page_mapper.map_initial_page_data()
    else:
        match request.form["form name"]:
            case "login":
                page_data = login_page_mapper.map_login()
            case "sign-up":
                page_data = login_page_mapper.map_sign_up()
            case "sign-up details":
                page_data = login_page_mapper.map_sign_up_details()
            case _:
                page_data = login_page_mapper.map_initial_page_data()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template("Login.html",
                           state=str(page_data.state),
                           message=page_data.message,
                           signing_up=page_data.signing_up)

load_dotenv()
environment = getenv("ENVIRONMENT")

if __name__ == '__main__':
    if environment == "Production" or environment == "Development":
        # Make available across all possible addresses when deployed on render
        serve(application, host='0.0.0.0', port=5000)
    else:
        # Make sure that Sqlite database is set up correctly with example data when run locally (but only if
        # the database does not already exist).
        if not path.isfile("persistence/HolidayBookingDatabase.db"):
            set_up_sqlite_database()

        # Limit application to localhost when run locally
        serve(application, host='127.0.0.1', port=5000)