from datetime import datetime

from flask import request, render_template, Blueprint, abort
from domains.user.UserRepository import UserRepository
from mappers.ResetPasswordPageMapper import ResetPasswordPageMapper
from persistence.DatabaseFactory import get_database
from werkzeug.exceptions import NotFound

reset_password_blueprint = Blueprint('reset_password_blueprint', __name__)
database = get_database()

user_repository = UserRepository(database)

reset_password_page_mapper = ResetPasswordPageMapper(user_repository)

@reset_password_blueprint.route("/reset", methods=["GET", "POST"])
def reset_password():

    try:
        reset_id = request.args.get("id")
        expiry_time = user_repository.get_expiry_time(reset_id)
        if request.method == "GET":
            # Check if id exists. If it does not, abort. Abort if we are past expiry date associated with id
            if expiry_time is None:
                abort(404)
            elif expiry_time < datetime.now():
                # clear expired values from table
                user_repository.clear_expiry_data(reset_id)
                abort(404)
            else:
                page_data = reset_password_page_mapper.map_initial_page_data()
        else:
            match request.form["form name"]:
                case "reset_password":
                    page_data = reset_password_page_mapper.map_reset_page_data(reset_id)
                case _:
                    page_data = reset_password_page_mapper.map_error()
    except NotFound as e:
        abort(404)
    except:
        page_data = reset_password_page_mapper.map_error()

    return render_template("ResetPassword.html",
                           state=page_data.state,
                           message=page_data.message)