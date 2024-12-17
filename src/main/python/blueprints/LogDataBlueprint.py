from flask import Blueprint, render_template, session, abort, request, redirect, url_for
from flask_login import login_required
from domains.user.UserRepository import UserRepository
from persistence.DatabaseFactory import get_database
from mappers.LoggingMapper import LoggingMapper

log_data_blueprint = Blueprint('log_data_blueprint', __name__)

database = get_database()

user_repository = UserRepository(database)

logging_mapper = LoggingMapper(user_repository)

@log_data_blueprint.route("/logs", methods=["GET", "POST"])
@login_required
def view_logs():

    user_details = user_repository.get_public_user_details(int(session["_user_id"]))

    if user_details is None:
        return redirect(url_for('login'))

    if user_details.account_type != "admin":
        abort(404)

    if request.method == "GET":
        page_data = logging_mapper.map_initial_page_data()
    else:
        page_data = logging_mapper.map_logout()

    if page_data.redirect is not None:
        return redirect(page_data.redirect)

    return render_template("LogData.html",
                           logs=page_data.logs,
                           logout_presses=page_data.logout_presses)