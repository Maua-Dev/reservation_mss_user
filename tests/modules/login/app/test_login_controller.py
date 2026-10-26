from unittest.mock import MagicMock

from src.modules.login.app.login_controller import LoginController
from src.modules.login.app.login_usecase import LoginUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestLoginController:
    def test_login_controller_missing_id_token(self):
        repo = UserRepositoryMock()
        usecase = LoginUsecase(repo=repo)
        controller = LoginController(usecase=usecase)

        response = controller(HttpRequest(body={}))

        assert response.status_code == 400
        assert response.body == "Field id_token is missing"

    def test_login_controller_wrong_type_id_token(self):
        repo = UserRepositoryMock()
        usecase = LoginUsecase(repo=repo)
        controller = LoginController(usecase=usecase)

        response = controller(HttpRequest(body={"id_token": 123}))

        assert response.status_code == 400
        assert "id_token" in response.body

    def test_login_controller_happy_path(self):
        repo = UserRepositoryMock()
        user = repo.users_list[0]

        usecase = MagicMock()
        usecase.return_value = ("signed.access.token", "a" * 64, user)
        controller = LoginController(usecase=usecase)

        response = controller(HttpRequest(body={"id_token": "aaa.bbb.ccc"}))

        assert response.status_code == 200
        assert response.body["access_token"] == "signed.access.token"
        assert response.body["user"]["name"] == user.name
        assert response.body["user"]["role"] == user.role.value
        assert "Set-Cookie" in response.headers
        assert response.headers["Set-Cookie"].startswith("refresh_token=")
        assert "HttpOnly" in response.headers["Set-Cookie"]
        assert "Secure" in response.headers["Set-Cookie"]
        assert "SameSite=None" in response.headers["Set-Cookie"]
        usecase.assert_called_once_with(id_token="aaa.bbb.ccc")
