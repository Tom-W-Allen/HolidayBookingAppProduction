from flask import render_template, Blueprint, request, session, redirect, url_for
from flask_login import login_required
from common.SecurityValidation import html_manipulation_detected
from mappers.EditProfilePageMapper import EditProfilePageMapper
from domains.user.UserRepository import UserRepository
from domains.request.RequestRepository import RequestRepository
from domains.project.ProjectRepository import ProjectRepository
from persistence.DatabaseFactory import get_database
from common.Logging import write_log

edit_profile_blueprint = Blueprint('edit_profile_blueprint', __name__)
database = get_database()

user_repository = UserRepository(database)
request_repository = RequestRepository(database)
project_repository = ProjectRepository(database)

edit_profile_page_mapper = EditProfilePageMapper(user_repository, request_repository, project_repository)


@edit_profile_blueprint.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    user_details = user_repository.get_public_user_details(int(session["_user_id"]))

    if user_details is None:
        return redirect(url_for('login'))

    try:
        if (str(session["refresh_page"])).upper() == "YES" or request.method == "GET":
            page_data = edit_profile_page_mapper.map_initial_page_data()
            session["refresh_page"] = "no"
        elif html_manipulation_detected():
            page_data = edit_profile_page_mapper.map_error()
            write_log(user_details.user_name, "HTML Manipulation", "HTML Manipulation attempted on Edit Profile Page")
        else:
            match request.form["form name"]:
                case "user selection":
                    page_data = edit_profile_page_mapper.map_select_user()
                case "initial edit profile":
                    page_data = edit_profile_page_mapper.map_confirm_changes()
                case "confirm changes":
                    page_data = edit_profile_page_mapper.map_execute_changes()
                case "delete account":
                    page_data = edit_profile_page_mapper.map_delete_user()
                case "approve account":
                    page_data = edit_profile_page_mapper.map_approve_user()
                case "log out":
                    page_data = edit_profile_page_mapper.map_logout()
                case _:
                    page_data = edit_profile_page_mapper.map_error()
    except Exception as ex:
        page_data = edit_profile_page_mapper.map_error()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template('EditProfile.html',
                           state=str(page_data.state),
                           message=page_data.message,
                           account_type=page_data.account_type,
                           selected_user=page_data.selected_user,
                           employee_list=page_data.employee_list,
                           user_details=page_data.user_details,
                           manager_list=page_data.manager_list,
                           approval_required=page_data.approval_required,
                           delete_button_presses=page_data.delete_button_presses,
                           approve_button_presses=page_data.approval_button_presses,
                           admin_approved = page_data.admin_approved,
                           base_id=page_data.base_id,
                           current_page='edit profile',
                           selected_manager=page_data.selected_manager,
                           logout_presses=page_data.logout_presses,
                           isProduction=user_repository.is_postgreSQL())

