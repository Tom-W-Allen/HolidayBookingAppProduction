from flask import request, render_template, Blueprint, session, redirect, url_for, abort
from flask_login import login_required
from common.SecurityValidation import html_manipulation_detected
from domains.project.ProjectRepository import ProjectRepository
from domains.user.UserRepository import UserRepository
from mappers.CreateProjectPageMapper import CreateProjectPageMapper
from persistence.DatabaseFactory import get_database

create_project_blueprint = Blueprint('create_project_blueprint', __name__)
database = get_database()

user_repository = UserRepository(database)
project_repository = ProjectRepository(database)

create_project_page_mapper = CreateProjectPageMapper(user_repository, project_repository)


@create_project_blueprint.route("/create-projects", methods=["GET", "POST"])
@login_required
def create_project():
    user_details = user_repository.get_public_user_details(int(session["_user_id"]))

    if user_details is None:
        return redirect(url_for('login'))

    if session["account_type"] == 'basic':
        abort(404)

    try:
        if (str(session["refresh_page"])).upper() == "YES" or request.method == "GET":
            page_data = create_project_page_mapper.map_initial_page_data()
            session["refresh_page"] = "no"
        elif html_manipulation_detected():
            page_data = create_project_page_mapper.map_error()
        else:
            match request.form["form name"]:
                case "create project":
                    page_data = create_project_page_mapper.map_create_project()
                case "log out":
                    page_data = create_project_page_mapper.map_logout()
                case _:
                    page_data = create_project_page_mapper.map_error()
    except:
        page_data = create_project_page_mapper.map_error()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template('CreateProject.html',
                           manager_list=page_data.manager_list,
                           state=str(page_data.state),
                           message=page_data.message,
                           current_page='create project',
                           account_type=session["account_type"],
                           logout_presses=page_data.logout_presses)
