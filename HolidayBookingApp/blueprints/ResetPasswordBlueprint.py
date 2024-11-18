from datetime import datetime

from flask import request, render_template, Blueprint, abort
from domains.user.UserRepository import UserRepository
from mappers.ResetPasswordPageMapper import ResetPasswordPageMapper
from persistence.DatabaseFactory import get_database

reset_password_blueprint = Blueprint('reset_password_blueprint', __name__)
database = get_database()

user_repository = UserRepository(database)

reset_password_page_mapper = ResetPasswordPageMapper(user_repository)

@reset_password_blueprint.route("/reset", methods=["GET", "POST"])
def reset_password():

    if request.method == "GET":
        # Check if id exists. If it does not, abort. Abort if we are past expiry date associated with id
        reset_id = request.args.get("id")
        expiry_time = user_repository.get_expiry_time(reset_id)

        if expiry_time is None:
            abort(404)
        elif expiry_time < datetime.now():
            # clear expired values from table
            abort(404)

        return render_template("ResetPassword.html")