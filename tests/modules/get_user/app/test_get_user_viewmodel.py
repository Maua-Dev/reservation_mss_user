from src.modules.get_user.app.get_user_viewmodel import GetUserViewModel
from src.modules.get_user.app.get_user_usecase import GetUserUseCase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock

class Test_GetUserViewModel:
    def test_get_user_viewmodel(self):
        repo = UserRepositoryMock()
        usecase = GetUserUseCase(repo=repo)
        user = usecase(repo.users_list[1].user_id)
        reponse = GetUserViewModel(user = user).to_dict()

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