from unittest.mock import MagicMock

from src.modules.refresh.app.refresh_controller import RefreshController
from src.modules.refresh.app.refresh_usecase import RefreshUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestRefreshController:
    def test_refresh_controller_missing_refresh_token(self):
        session_repo = SessionRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)
        controller = RefreshController(usecase=usecase)

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert response.body == "Field refresh_token is missing"

    def test_refresh_controller_wrong_type_refresh_token(self):
        session_repo = SessionRepositoryMock()
        user_repo = UserRepositoryMock()
        usecase = RefreshUsecase(session_repo=session_repo, user_repo=user_repo)
        controller = RefreshController(usecase=usecase)

        response = controller(HttpRequest(body={"refresh_token": 123}))

        assert response.status_code == 400
        assert "refresh_token" in response.body

    def test_refresh_controller_happy_path_body(self):
        usecase = MagicMock()
        usecase.return_value = ("signed.access.token", "signed.refresh.token")
        controller = RefreshController(usecase=usecase)

        response = controller(HttpRequest(body={"refresh_token": "aaa.bbb.ccc"}))

        assert response.status_code == 200
        assert response.body["access_token"] == "signed.access.token"
        assert response.body["message"] == "Tokens refreshed successfully"
        assert "refresh_token" not in response.body
        assert "Set-Cookie" in response.headers
        assert response.headers["Set-Cookie"].startswith("refresh_token=")
        assert "HttpOnly" in response.headers["Set-Cookie"]
        assert "Secure" in response.headers["Set-Cookie"]
        assert "SameSite=None" in response.headers["Set-Cookie"]
        usecase.assert_called_once_with(refresh_token="aaa.bbb.ccc")

    def test_refresh_controller_happy_path_cookie(self):
        usecase = MagicMock()
        usecase.return_value = ("signed.access.token", "signed.refresh.token")
        controller = RefreshController(usecase=usecase)

        response = controller(
            HttpRequest(
                body={},
                headers={"Cookie": "refresh_token=aaa.bbb.ccc"},
            )
        )

        assert response.status_code == 200
        assert response.body["access_token"] == "signed.access.token"
        assert "Set-Cookie" in response.headers
        assert "SameSite=None" in response.headers["Set-Cookie"]
        usecase.assert_called_once_with(refresh_token="aaa.bbb.ccc")
