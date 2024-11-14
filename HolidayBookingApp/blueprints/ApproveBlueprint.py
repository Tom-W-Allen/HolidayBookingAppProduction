from flask import request, render_template, Blueprint, session, redirect, url_for, abort
from flask_login import login_required
from common.SecurityValidation import html_manipulation_detected
from domains.request.RequestRepository import RequestRepository
from domains.user.UserRepository import UserRepository
from mappers.ApproveHolidayPageMapper import ApproveHolidayPageMapper
from persistence.DatabaseFactory import get_database

approve_blueprint = Blueprint('approve_blueprint', __name__)

database = get_database(True)

request_repository = RequestRepository(database)
user_repository = UserRepository(database)

approve_holiday_page_mapper = ApproveHolidayPageMapper(request_repository, user_repository)


@approve_blueprint.route("/approve", methods=["GET", "POST"])
@login_required
def approve_holiday():

    user_details = user_repository.get_public_user_details(int(session["_user_id"]))

    if user_details is None:
        return redirect(url_for('login'))

    if session["account_type"] == 'basic':
        abort(404)

    try:
        if (str(session["refresh_page"])).upper() == "YES" or request.method == "GET":
            page_data = approve_holiday_page_mapper.map_initial_page_data()
            session["refresh_page"] = "no"
        elif html_manipulation_detected():
            page_data = approve_holiday_page_mapper.map_error()
        else:
            match request.form["form name"]:
                case "user selection":
                    page_data = approve_holiday_page_mapper.map_admin_user_selection()
                case "confirm approve or reject":
                    page_data = approve_holiday_page_mapper.map_confirm_approve_or_reject_request()
                case "approve or reject request":
                    page_data = approve_holiday_page_mapper.map_approve_or_reject_request()
                case "log out":
                    page_data = approve_holiday_page_mapper.map_logout()
                case _:
                    page_data = approve_holiday_page_mapper.map_error()
    except Exception as ex:
        page_data = approve_holiday_page_mapper.map_error()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template("HolidayApproval.html",
                           state=str(page_data.state),
                           message=page_data.message,
                           employee_list=page_data.employee_list,
                           selected_user=page_data.selected_user,
                           request_list=page_data.request_list,
                           approval_required=page_data.approval_required,
                           approval_state=page_data.approval_state,
                           account_type=page_data.account_type,
                           current_page='approve',
                           logout_presses=page_data.logout_presses)
