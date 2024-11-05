
from src.modules.update_user.app.update_user_controller import UpdateUserController
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class TestUpdateUserController:

    def test_update_user_controller_missing_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            "confirm_user": True,
            "role": "ADMIN"
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field user_id is missing"

    def test_update_user_controller_wrong_type_user_id(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": 123, 
            "confirm_user": True,
            "role": "ADMIN"
        })

        response = controller(request)

        assert response.status_code == 400
        assert "Field user_id isn't in the right type." in response.body
        assert "Received: int." in response.body
        assert "Expected: str" in response.body


    def test_update_user_controller_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "non-existent-id",
            "confirm_user": True,
            "role": "ADMIN"
        })

        response = controller(request)

        assert response.status_code == 404
        assert response.body == "User not found"

    def test_update_user_controller_invalid_role(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "93bc6ada-c0d1-7054-26ab-e17414c48ae3",
            "confirm_user": True,
            "role": "INVALID_ROLE"  # Invalid role
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field role is not valid"
