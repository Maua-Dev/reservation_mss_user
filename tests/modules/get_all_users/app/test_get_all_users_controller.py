from src.modules.get_all_users.app.get_all_users_controller import GetAllUserSController
from src.modules.get_all_users.app.get_all_users_usecase import GetAllUserUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_GetAllUsersController:
    def test_get_all_users_controller(self):
        repo = UserRepositoryMock()
        usecase = GetAllUserUsecase(repo)
        controller = GetAllUserSController(usecase)
        request = HttpRequest(headers={
            'user_from_authorizer':
                {
                    "id": "93bc6ada-c0d1-7054-26ab-e17414c48ae3",
                    "name":"Rodas Rodas",
                    "email":"rodas@gmail.com"
                }
        })

        response = controller(request)

        assert response.status_code == 200
        assert response.body['users'][0]['user_id'] == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        assert response.body['users'][0]['name'] == "Rodas Rodas"
        assert response.body['users'][0]['email'] == "rodas@gmail.com"
        assert response.body['users'][0]['role'] == 'ADMIN'
        assert response.body['users'][0]['confirm_user'] == True
        assert response.body['users'][0]['ra'] == None
        
        