from flask import request, session

def html_manipulation_detected():

    if request.form["form name"] == "log out":
        return False

    admin_only_forms = ["user selection", "delete account"]

    admin_form_selected = "form name" in request.form.keys() and request.form["form name"] in admin_only_forms

    if admin_form_selected and session["account_type"] != "admin":
        return True

    if "selected user" in request.form.keys():
        # If user is not an admin and the selected user field does not match their session id, then html fields
        # must have been changed. Do not allow further processing.
        incorrect_user_selected = not (session["account_type"] == 'admin' or
                                  (str(request.form["selected user"]) == str(session["_user_id"])))
    else:
        incorrect_user_selected = False

    return incorrect_user_selected