from src.modules.create_session.app.create_session_controller import CreateSessionController
from src.modules.create_session.app.create_session_usecase import CreateSessionUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestCreateSessionController:

    def _controller(self):
        repo = SessionRepositoryMock()
        usecase = CreateSessionUsecase(repo=repo)
        return CreateSessionController(usecase=usecase)

    def test_create_session_controller(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": "00000000-0000-0000-0000-000000000003",
                "mail": "teste@gmail.com",
                "displayName": "Usuario Teste",
            },
            "refresh_token": "novo_token"
        })

        response = controller(request)

        assert response.status_code == 201
        assert response.body['session']['user_id'] == "00000000-0000-0000-0000-000000000003"
        assert response.body['session']['refresh_token'] == "novo_token"
        assert response.body['message'] == "the session was created successfully"

    def test_create_session_controller_denied(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "refresh_token": "novo_token"
        })

        response = controller(request)

        assert response.status_code == 404

    def test_create_session_controller_missing_refresh_token(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": "00000000-0000-0000-0000-000000000003",
                "mail": "teste@gmail.com",
                "displayName": "Usuario Teste",
            }
        })

        response = controller(request)

        assert response.status_code == 400

    def test_create_session_controller_duplicated(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": "00000000-0000-0000-0000-000000000001",
                "mail": "teste@gmail.com",
                "displayName": "Usuario Teste",
            },
            "refresh_token": "novo_token"
        })

        response = controller(request)

        assert response.status_code == 400

    def test_create_session_controller_entity_error(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": "00000000-0000-0000-0000-000000000003",
                "mail": "teste@gmail.com",
                "displayName": "Usuario Teste",
            },
            "refresh_token": 123
        })

        response = controller(request)

        assert response.status_code == 400