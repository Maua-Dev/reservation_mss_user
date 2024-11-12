from src.modules.delete_user.app.delete_user_controller import DeleteUserController
from src.modules.delete_user.app.delete_user_usecase import DeleteUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestDeleteUserController:

    def test_delete_user_controller(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(headers={
            "user_from_authorizer":
                {
                    "id": "93bc6ada-c0d1-7054-26ab-e17414c48ae5",
                    "email": "26.96379-5@maua.br",
                    "name": "Rubio Rosa",
                }
        })

        response = controller(request)

        assert response.status_code == 200

    def test_delete_user_controller_denied(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(headers={
            "headers":
                {
                    "headerkey1": "headerval1",
                }
        })

        response = controller(request)

        assert response.status_code == 404

    def test_delete_user_controller_found_user(self):
        repo = UserRepositoryMock()
        usecase = DeleteUserUsecase(repo=repo)
        controller = DeleteUserController(usecase=usecase)

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "name": "Rubio Rosa",
                "email": "26.96379-5@maua.br",
                "id": "93bc6ada-c0d1-7054-26ab-e17414c"
            }
        })

        response = controller(request)

        assert response.status_code == 400