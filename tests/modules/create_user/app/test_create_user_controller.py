from src.modules.create_user.app.create_user_controller import CreateUserController
from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestCreateUserController:

    def test_create_user_controller(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(headers={
            "user_from_authorizer":
                {
                    "id": "93bc6ada-c0d1-7054-26ab-e17414c48fe5",
                    "mail": "52.00847-4@maua.br",
                    "displayName": "Jao do Bao",
                }
        })

        response = controller(request)

        assert response.status_code == 201

    def test_create_user_controller_denied(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(headers={
            "headers":
                {
                    "headerkey1": "headerval1",
                }
        })

        response = controller(request)

        assert response.status_code == 404

    def test_create_user_controller_found_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "displayName": "Vini Berti",
                "mail": "50.00847-4@maua.br",
                "id": "93bc6ada-c0d1-8754-26ab-e17414c48ae7"
            }
        })

        response = controller(request)

        assert response.status_code == 400

    def test_create_user_controller_raise_entity_error(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo=repo)
        controller = CreateUserController(usecase=usecase)

        request = HttpRequest(headers={
            "user_from_authorizer": {
                "displayName": 1,
                "mail": "50.00847-4@maua.br",
                "id": "93bc6ada-c0d1-8754-26ab-e17414c48ae7"
            }
        })

        response = controller(request)

        assert response.status_code == 400


