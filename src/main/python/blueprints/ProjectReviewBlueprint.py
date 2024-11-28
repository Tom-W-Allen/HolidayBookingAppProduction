from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required
from common.SecurityValidation import html_manipulation_detected
from domains.project.ProjectRepository import ProjectRepository
from domains.user.UserRepository import UserRepository
from mappers.ReviewProjectPageMapper import ReviewProjectPageMapper
from persistence.DatabaseFactory import get_database

project_review_blueprint = Blueprint('project_review_blueprint', __name__)
database = get_database()

project_repository = ProjectRepository(database)
user_repository = UserRepository(database)

review_project_page_mapper = ReviewProjectPageMapper(project_repository)


@project_review_blueprint.route('/review-projects', methods=["GET", "POST"])
@login_required
def review_projects():

    user_details = user_repository.get_public_user_details(int(session["_user_id"]))

    if user_details is None:
        return redirect(url_for('login'))

    try:
        if (str(session["refresh_page"])).upper() == "YES" or request.method == "GET":
            page_data = review_project_page_mapper.map_initial_page_data()
            session["refresh_page"] = "no"
        elif html_manipulation_detected():
            page_data = review_project_page_mapper.map_error()
        else:
            match request.form["form name"]:
                case "review":
                    page_data = review_project_page_mapper.map_project_selection()
                case "add employee":
                    page_data = review_project_page_mapper.map_add_employee()
                case "confirm removal":
                    page_data = review_project_page_mapper.map_confirm_removal()
                case "remove employee":
                    page_data = review_project_page_mapper.map_remove_employee()
                case "log out":
                    page_data = review_project_page_mapper.map_logout()
                case _:
                    page_data = review_project_page_mapper.map_error()
    except Exception as e:
        page_data = review_project_page_mapper.map_error()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template('ReviewProjects.html',
                           state=str(page_data.state),
                           message=page_data.message,
                           project_list=page_data.project_list,
                           selected_project=page_data.selected_project,
                           enrolled_employees=page_data.enrolled_employees,
                           available_employees=page_data.available_employees,
                           add_employee_button_presses=page_data.add_employee_button_presses,
                           selected_employee_id=page_data.selected_employee_id,
                           remove_employee=page_data.remove_employee,
                           account_type=page_data.account_type,
                           current_page='review projects',
                           logout_presses=page_data.logout_presses)
