from flask import render_template, Blueprint, request, abort, redirect
from persistence.DatabaseFactory import get_database
from mappers.ForgottenPasswordMapper import ForgottenPasswordMapper
from domains.user.UserRepository import UserRepository

forgotten_password_blueprint = Blueprint('forgotten_password_blueprint', __name__)
database = get_database()

user_repository = UserRepository(database)

forgotten_password_page_mapper = ForgottenPasswordMapper(user_repository,)


@forgotten_password_blueprint.route("/forgotten-password", methods=["GET", "POST"])
def send_email():
    if not user_repository.is_postgreSQL():
        abort(404, "The application is being run in a local environment. Email addresses cannot be entered or changed")

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