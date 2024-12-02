from unittest import TestCase
from flask import session # Session needs to be directly imported so that data is kept when calling functions

from application import application
from common.SecurityValidation import html_manipulation_detected

admin_only_forms = ["user selection", "delete account"]

class SecurityTests(TestCase):
    def test_html_manipulation_detected_returns_false_when_form_name_is_log_out(self):

        with application.test_request_context(data={"form name": "log out"}):
            actual_result = html_manipulation_detected()

            self.assertFalse(actual_result)

    def test_html_manipulation_detected_returns_true_when_admin_form_selected_and_user_not_admin(self):

        for form_name in admin_only_forms:
            with self.subTest(form_name):
                with application.test_request_context(data={"form name": form_name}):
                    session["account_type"] = "basic"
                    actual_result = html_manipulation_detected()

                self.assertTrue(actual_result)

    def test_html_manipulation_detected_returns_false_when_form_is_not_admin_only(self):

        with application.test_request_context(data={"form name": "test"}):
            session["account_type"] = "basic"
            actual_result = html_manipulation_detected()

        self.assertFalse(actual_result)

    def test_html_manipulation_detected_returns_true_when_selected_user_mismatch_and_user_basic(self):

        with application.test_request_context(data={"form name": "test",
                                                    "selected user": 1}):
            session["account_type"] = "basic"
            session["_user_id"] = "2"
            actual_result = html_manipulation_detected()

        self.assertTrue(actual_result)

    def test_html_manipulation_detected_returns_false_when_selected_user_match_and_user_basic(self):

        with application.test_request_context(data={"form name": "test",
                                                    "selected user": 1}):
            session["account_type"] = "basic"
            session["_user_id"] = "1"
            actual_result = html_manipulation_detected()

        self.assertFalse(actual_result)

    def test_html_manipulation_detected_returns_false_when_selected_user_mismatch_and_user_admin(self):

        with application.test_request_context(data={"form name": "test",
                                                    "selected user": 1}):
            session["account_type"] = "admin"
            session["_user_id"] = "2"
            actual_result = html_manipulation_detected()

        self.assertFalse(actual_result)
