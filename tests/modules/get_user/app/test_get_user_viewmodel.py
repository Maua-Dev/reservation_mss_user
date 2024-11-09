from src.modules.get_user.app.get_user_viewmodel import GetUserViewmodel
from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetUserViewmodel:
    def test_get_user_viewmodel(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo)
        user = usecase(repo.users_list[1].user_id)
        reponse = GetUserViewmodel(user = user).to_dict()

        expected = {
            "user": {
                "name" : "Rubio Rosa",
                "email" : "26.96379-5@maua.br",
                "user_id" : "93bc6ada-c0d1-7054-26ab-e17414c48ae5",
                "ra" : "26.96379-5",
                "role" : "ADMIN",
                "confirm_user" : False
            },
            "message": "the user was retrieved"
        }

        assert reponse == expected

        
    def test_get_user_viewmodel_professor(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo)
        user = usecase(repo.users_list[3].user_id)
        response = GetUserViewmodel(user=user).to_dict()

        expected = {
            "user": {
                "name": "Giovanna Ehobeckas",
                "email": "gi@hotmail.com",
                "user_id": "93bc6ada-c0d1-7054-26ab-e17454c48ae6",
                "ra": None,
                "role": "PROFESSOR",
                "confirm_user": True
            },
            "message": "the user was retrieved"
        }

        assert response == expected