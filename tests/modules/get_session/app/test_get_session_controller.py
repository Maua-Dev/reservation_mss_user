from src.modules.get_session.app.get_session_usecase import GetSessionUsecase
from src.modules.get_session.app.get_session_controller import GetSessionController
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest


class TestGetSessionController:

    def test_get_session_controller(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo=repo)
        controller = GetSessionController(usecase=usecase)
        request = HttpRequest(headers={
            "user_from_authorizer":
                {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "name": "Usuario Teste",
                    "mail": "teste@gmail.com"
                }
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['session']['user_id'] == "00000000-0000-0000-0000-000000000001"
        assert response.body['session']['refresh_token'] == "refresh_token_1"
        assert response.body['message'] == "the session was retrieved"

    def test_get_session_controller_session_not_found(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo=repo)
        controller = GetSessionController(usecase=usecase)
        request = HttpRequest(headers={
            "user_from_authorizer":
                {
                    "id": "00000000-0000-0000-0000-000000000099",
                    "name": "Usuario Teste",
                    "mail": "teste@gmail.com"
                }
        })

        response = controller(request)

        assert response.status_code == 404
        assert response.body == "No items found for user_id"

    def test_get_session_controller_denied(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo=repo)
        controller = GetSessionController(usecase=usecase)
        request = HttpRequest(headers={})

        response = controller(request)

        assert response.status_code == 400

    def test_get_session_controller_invalid_user_id(self):
        repo = SessionRepositoryMock()
        usecase = GetSessionUsecase(repo=repo)
        controller = GetSessionController(usecase=usecase)
        request = HttpRequest(headers={
            "user_from_authorizer":
                {
                    "id": "not-a-uuid",
                    "name": "Usuario Teste",
                    "mail": "teste@gmail.com"
                }
        })

        response = controller(request)

        assert response.status_code == 500