from src.modules.get_user.app.get_user_usecase import GetUserUseCase
from src.modules.get_user.app.get_user_controller import GetUserController
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestGetUserController:
    def test_get_user_controller(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)
        request = HttpRequest(headers={
            "user_from_authorizer":
                {
                    "id": "93bc6ada-c0d1-7054-26ab-e17414c48ae3",
                    "name":"Rodas Rodas",
                    "mail":"rodas@gmail.com"
                }
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['user']['user_id'] == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        assert response.body['user']['name'] == "Rodas Rodas"
        assert response.body['user']['mail'] == "rodas@gmail.com"
        assert response.body['user']['role'] == "ADMIN"
        assert response.body['user']['confirm_user'] == True
        assert response.body['user']['ra'] == None

    def test_get_user_controller_missing_id(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)
        request = HttpRequest(body={
            "name": "Leo Iorio",
            "email": "29.91279-6@maua.br",
            "ra": "29.91279-6",
            "role": "STUDENT",
            "confirm_user": True
        })

        response = controller(request)

        assert response.status_code == 400
        assert response.body == "Field user_id is missing" 


    def test_get_user_controller_wrong_type_id(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)
        request = HttpRequest(body={
            "user_id": 123,
            "name": "Leo Iorio",
            "email": "29.91279-6@maua.br",
            "ra": "29.91279-6",
            "role": "STUDENT",
            "confirm_user": True
        })

        response = controller(request)

        assert response.status_code == 400
        assert "Field user_id isn't in the right type." in response.body
        assert "Received: int." in response.body
        assert "Expected: str" in response.body


    def test_get_user_controller_user_not_found(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        controller = GetUserController(usecase=usecase)
        request = HttpRequest(body={
            "user_id": "93bc6ada-c0d1-7054-26ab-e17414c98ae5",
            "name": "Leo Iorio",
            "email": "29.91279-6@maua.br",
            "ra": "29.91279-6",
            "role": "STUDENT",
            "confirm_user": True
        })

        response = controller(request)

        assert response.status_code == 404
        assert response.body == "No items found for user_id"
            