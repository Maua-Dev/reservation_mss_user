import uuid

from src.modules.delete_session.app.delete_session_controller import DeleteSessionController
from src.modules.delete_session.app.delete_session_usecase import DeleteSessionUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestDeleteSessionController:

    def _controller(self):
        repo = SessionRepositoryMock()
        usecase = DeleteSessionUsecase(repo=repo)
        return DeleteSessionController(usecase=usecase)

    def test_delete_session_controller(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": "00000000-0000-0000-0000-000000000001"
            }
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['session']['user_id'] == "00000000-0000-0000-0000-000000000001"
        assert response.body['session']['refresh_token'] == "refresh_token_1"
        assert response.body['message'] == "the session was deleted successfully"

    def test_delete_session_controller_denied(self):
        controller = self._controller()

        request = HttpRequest(headers={})

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Authorizer denied token, user was not returned from it"

    def test_delete_session_controller_wrong_type(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": 123
            }
        })

        response = controller(request)

        assert response.status_code == 400

    def test_delete_session_controller_invalid_uuid(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": "not-a-uuid"
            }
        })

        response = controller(request)

        assert response.status_code == 400

    def test_delete_session_controller_not_found(self):
        controller = self._controller()

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "id": str(uuid.uuid4())
            }
        })

        response = controller(request)

        assert response.status_code == 404