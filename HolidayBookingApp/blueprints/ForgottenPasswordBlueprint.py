from flask import render_template, Blueprint, request, session, redirect
from persistence.DatabaseFactory import get_database
from common.SecurityValidation import html_manipulation_detected
from mappers.ForgottenPasswordMapper import ForgottenPasswordMapper
from domains.user.UserRepository import UserRepository
from domains.request.RequestRepository import RequestRepository
from domains.project.ProjectRepository import ProjectRepository

forgotten_password_blueprint = Blueprint('forgotten_password_blueprint', __name__)

connection_string = "persistence/HolidayBookingDatabase.db"

database = get_database()

user_repository = UserRepository(database)
request_repository = RequestRepository(database)
project_repository = ProjectRepository(connection_string, database)

forgotten_password_page_mapper = ForgottenPasswordMapper(user_repository, request_repository, project_repository)


@forgotten_password_blueprint.route("/forgotten-password", methods=["GET", "POST"])
def send_email():

    try:
        if request.method == "GET":
            page_data = forgotten_password_page_mapper.map_initial_page_data()
        else:
            match request.form["form name"]:
                case "reset_password":
                    page_data = forgotten_password_page_mapper.map_send_email()
                case _:
                    page_data = forgotten_password_page_mapper.map_error()
    except:
        page_data = forgotten_password_page_mapper.map_error()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template('ForgottenPassword.html',
                           state=str(page_data.state),
                           message=page_data.message,
                           successful_reset=page_data.successful_reset)