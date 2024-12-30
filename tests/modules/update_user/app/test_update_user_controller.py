
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
            "new_confirm_user": True,
            "new_role": "ADMIN"
        })

        response = controller(request)

        assert response.status_code == 400
        assert "Field user_id isn't in the right type." in response.body
        assert "Received: <class 'int'>" in response.body
        assert "Expected: <class 'str'>" in response.body


    def test_update_user_controller_invalid_role(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        request = HttpRequest(body={
            "user_id": "93bc6ada-c0d1-7054-26ab-e17414c48ae3",
            "new_confirm_user": True,
            "new_role": "INVALID_ROLE"  
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field new_role is not valid"

    def test_update_user_controller_success(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        controller = UpdateUserController(usecase=usecase)

        user_id = "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        
        request = HttpRequest(body={
            "user_id": user_id,
            "new_confirm_user": True,
            "new_role": "PROFESSOR"
        })
        
        response = controller(request)
        
        assert response.status_code == 200
        assert "user_id" in response.body["updated_user"]
        assert response.body["updated_user"]["user_id"] == user_id
        assert response.body["updated_user"]["role"] == "PROFESSOR"
        assert response.body["updated_user"]["confirm_user"] == True

