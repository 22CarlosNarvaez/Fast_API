import unittest
from unittest.mock import call, patch

import requests
from fastapi.testclient import TestClient

from src.views.main import app
from src.views import views


class ConsoleClientTests(unittest.TestCase):
    def test_console_operations_cover_all_menu_options(self):
        inputs = [
            "DOC-1",
            "Ana",
            "Pérez",
            "ana@example.com",
            "20",
            "Desarrollo",
            "12345",
            "trainee-id",
            "trainee-id",
            "DOC-2",
            "",
            "",
            "",
            "",
            "",
            "",
            "trainee-id",
            "s",
        ]
        with (
            patch("src.views.views.send_request") as send_request,
            patch("src.views.views.show_result"),
            patch("builtins.input", side_effect=inputs),
        ):
            views.show_home()
            views.create_trainee()
            views.list_trainees()
            views.get_trainee()
            views.update_trainee()
            views.delete_trainee()

        self.assertEqual(
            send_request.call_args_list,
            [
                call("GET", "/"),
                call(
                    "POST",
                    "/trainees",
                    {
                        "document": "DOC-1",
                        "firstname": "Ana",
                        "lastname": "Pérez",
                        "email": "ana@example.com",
                        "age": 20,
                        "program": "Desarrollo",
                        "record_number": "12345",
                    },
                ),
                call("GET", "/trainees"),
                call("GET", "/trainees/trainee-id"),
                call("PUT", "/trainees/trainee-id", {"document": "DOC-2"}),
                call("DELETE", "/trainees/trainee-id"),
            ],
        )

    def test_menu_options_are_consecutive_without_database_health_option(self):
        self.assertEqual(list(views.OPTIONS), ["1", "2", "3", "4", "5", "6"])
        self.assertNotIn("Estado de MongoDB", {
            label for label, _ in views.OPTIONS.values()
        })

    @patch("src.views.views.requests.request")
    def test_send_request_uses_base_url_json_and_timeout(self, request):
        views.send_request("POST", "/trainees", {"firstname": "Ana"})

        request.assert_called_once_with(
            "POST",
            f"{views.API_URL}/trainees",
            json={"firstname": "Ana"},
            timeout=10,
        )

    @patch(
        "src.views.views.requests.request",
        side_effect=requests.ConnectionError("connection refused"),
    )
    def test_send_request_reports_connection_errors(self, _request):
        with patch("builtins.print") as print_output:
            response = views.send_request("GET", "/")

        self.assertIsNone(response)
        self.assertIn("connection refused", print_output.call_args.args[0])

    def test_ask_id_reprompts_when_empty(self):
        with patch("builtins.input", side_effect=["", "trainee-id"]):
            trainee_id = views.ask_id()

        self.assertEqual(trainee_id, "trainee-id")


class ApiEndpointTests(unittest.TestCase):
    def test_root_and_database_dependent_endpoints_return_clear_statuses(self):
        with (
            patch.object(app.state, "database", None),
            patch("src.templates.controllers.collection", None),
            TestClient(app) as client,
        ):
            self.assertEqual(client.get("/").status_code, 200)
            self.assertEqual(client.get("/health/db").status_code, 503)
            self.assertEqual(client.get("/trainees").status_code, 503)
            self.assertEqual(
                client.post(
                    "/trainees",
                    json={
                        "document": "DOC-1",
                        "firstname": "Ana",
                        "lastname": "Pérez",
                        "email": "ana@example.com",
                        "age": 20,
                        "program": "Desarrollo",
                        "record_number": "12345",
                    },
                ).status_code,
                503,
            )
            self.assertEqual(
                client.put(
                    "/trainees/507f1f77bcf86cd799439011",
                    json={"firstname": "Ana"},
                ).status_code,
                503,
            )
            self.assertEqual(
                client.delete(
                    "/trainees/507f1f77bcf86cd799439011"
                ).status_code,
                503,
            )

    def test_invalid_trainee_id_returns_not_found(self):
        with (
            patch("src.templates.controllers.collection"),
            TestClient(app) as client,
        ):
            response = client.get("/trainees/not-an-object-id")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "ID de aprendiz no válido")


if __name__ == "__main__":
    unittest.main()
