from flask import Blueprint, render_template, session, request, redirect, url_for, abort
from flask_login import login_required
from common.SecurityValidation import html_manipulation_detected
from domains.user.UserRepository import UserRepository
from domains.request.RequestRepository import RequestRepository
from mappers.RequestPageMapper import RequestPageMapper
from persistence.DatabaseFactory import get_database

request_blueprint = Blueprint('request_blueprint', __name__)

connection_string = "persistence/HolidayBookingDatabase.db"

database = get_database()

request_repository = RequestRepository(database)
user_repository = UserRepository(database)

request_page_mapper = RequestPageMapper(user_repository, request_repository)


@request_blueprint.route("/request", methods=["GET", "POST"])
@login_required
def request_holiday():

    user_details = user_repository.get_public_user_details(int(session["_user_id"]))

    if user_details is None:
        return redirect(url_for('login'))

    if session["account_type"] == 'manager':
        abort(404)

    try:
        if (str(session["refresh_page"])).upper() == "YES" or request.method == "GET":
            page_data = request_page_mapper.map_initial_page_data()
            session["refresh_page"] = "no"
        elif html_manipulation_detected():
            page_data = request_page_mapper.map_error()
        else:
            match request.form["form name"]:
                case "user selection":
                    page_data = request_page_mapper.map_admin_selection()
                case "date selection":
                    page_data = request_page_mapper.map_date_submission()
                case "date confirmation":
                    page_data = request_page_mapper.map_date_confirmation()
                case "confirm cancel":
                    page_data = request_page_mapper.map_confirm_cancel()
                case "cancel request":
                    page_data = request_page_mapper.map_cancel_request()
                case "log out":
                    page_data = request_page_mapper.map_logout()
                case _:
                    page_data = request_page_mapper.map_error()
    except Exception as ex:
        page_data = request_page_mapper.map_error()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template("HolidayRequest.html",
                           state=str(page_data.state),
                           message=page_data.message,
                           remaining_holidays=page_data.remaining_holidays,
                           pending_holidays=page_data.pending_holidays,
                           selected_dates=page_data.selected_dates,
                           account_type=page_data.account_type,
                           user_id=page_data.user_id,
                           basic_users=page_data.basic_users,
                           request_list=page_data.request_list,
                           approval_required=page_data.approval_required,
                           manager=page_data.manager,
                           base_user=page_data.base_user,
                           current_page='request',
                           logout_presses=page_data.logout_presses)
