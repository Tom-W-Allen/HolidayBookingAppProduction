from flask import Blueprint, render_template, session, redirect, url_for, request
from flask_login import login_required
from common.SecurityValidation import html_manipulation_detected
from domains.user.UserRepository import UserRepository
from domains.request.RequestRepository import RequestRepository
from domains.project.ProjectRepository import ProjectRepository
from mappers.HomePageMapper import HomePageMapper
from persistence.DatabaseFactory import get_database

home_blueprint = Blueprint('home_blueprint', __name__)
database = get_database()

user_repository = UserRepository(database)
request_repository = RequestRepository(database)
project_repository = ProjectRepository(database)

home_page_mapper = HomePageMapper(user_repository, request_repository, project_repository)


@home_blueprint.route('/', methods=["GET", "POST"])
@login_required
def home_page():

    user_details = user_repository.get_public_user_details(int(session["_user_id"]))

    if user_details is None:
        return redirect(url_for('login'))
    try:
        if (str(session["refresh_page"])).upper() == "YES" or request.method == "GET":
            page_data = home_page_mapper.map_initial_page_data()
            session["refresh_page"] = "no"
        elif html_manipulation_detected():
            page_data = home_page_mapper.map_error()
        else:
            match request.form["form name"]:
                case "log out":
                    page_data = home_page_mapper.map_logout()
                case _:
                    page_data = home_page_mapper.map_error()
    except:
        page_data = home_page_mapper.map_error()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template("Home.html",
                           current_page='home',
                           state=str(page_data.state),
                           message=page_data.message,
                           account_type=page_data.account_type,
                           user_details=page_data.user_details,
                           total_projects=page_data.total_projects,
                           total_users=page_data.total_users,
                           rejected_requests=page_data.rejected_requests,
                           cancelled_requests=page_data.cancelled_requests,
                           pending_requests=page_data.pending_requests,
                           approved_requests=page_data.approved_requests,
                           upcoming_holidays=page_data.upcoming_holidays,
                           logout_presses=page_data.logout_presses)
