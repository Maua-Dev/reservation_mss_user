import uuid

from src.modules.update_session.app.update_session_controller import UpdateSessionController
from src.modules.update_session.app.update_session_usecase import UpdateSessionUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.session_repository_mock import SessionRepositoryMock


class TestUpdateSessionController:

    def _controller(self):
        repo = SessionRepositoryMock()
        usecase = UpdateSessionUsecase(repo=repo)
        return UpdateSessionController(usecase=usecase)

    def test_update_session_controller_success(self):
        controller = self._controller()

        request = HttpRequest(
            headers={
                "user_from_authorizer": {
                    "id": "00000000-0000-0000-0000-000000000001"
                }
            },
            body={
                "new_refresh_token": "token_novo"
            }
        )

        response = controller(request)

        assert response.status_code == 200
        assert response.body["updated_session"]["user_id"] == "00000000-0000-0000-0000-000000000001"
        assert response.body["updated_session"]["refresh_token"] == "token_novo"
        assert response.body["message"] == "the session was updated"

    def test_update_session_controller_denied(self):
        controller = self._controller()

        request = HttpRequest(headers={})

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Authorizer denied token, user was not returned from it"

    def test_update_session_controller_wrong_type_user_id(self):
        controller = self._controller()

        request = HttpRequest(
            headers={
                "user_from_authorizer": {
                    "id": 123
                }
            },
            body={
                "new_refresh_token": "token_novo"
            }
        )

        response = controller(request)

        assert response.status_code == 400
        assert "Field user_id isn't in the right type." in response.body

    def test_update_session_controller_missing_refresh_token(self):
        controller = self._controller()

        request = HttpRequest(
            headers={
                "user_from_authorizer": {
                    "id": "00000000-0000-0000-0000-000000000001"
                }
            }
        )

        response = controller(request)

        assert response.status_code == 400

    def test_update_session_controller_wrong_type_refresh_token(self):
        controller = self._controller()

        request = HttpRequest(
            headers={
                "user_from_authorizer": {
                    "id": "00000000-0000-0000-0000-000000000001"
                }
            },
            body={
                "new_refresh_token": 123
            }
        )

        response = controller(request)

        assert response.status_code == 400
        assert "Field new_refresh_token isn't in the right type." in response.body

    def test_update_session_controller_not_found(self):
        controller = self._controller()

        request = HttpRequest(
            headers={
                "user_from_authorizer": {
                    "id": str(uuid.uuid4())
                }
            },
            body={
                "new_refresh_token": "token_novo"
            }
        )

        response = controller(request)

        assert response.status_code == 404