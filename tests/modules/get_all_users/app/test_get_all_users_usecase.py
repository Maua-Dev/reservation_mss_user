from src.modules.get_all_users.app.get_all_users_usecase import GetAllUserUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_get_all_users_usecase:
    def test_get_all_users(self):
        repo = UserRepositoryMock()

        usecase = GetAllUserUsecase(repo)

        users = usecase()

        assert len(users) == 8
        assert users[0].name == "Rodas Rodas"
        assert users[0].email == "rodas@gmail.com"
        assert users[0].user_id == "93bc6ada-c0d1-7054-26ab-e17414c48ae3"
        assert users[0].ra == None
        assert users[0].role == ROLE.ADMIN
        assert users[0].confirm_user == True

    def test_get_all_users_no_items(self):
        repo = UserRepositoryMock()

        usecase = GetAllUserUsecase(repo)

        repo.users_list = []

        try:
            usecase()
        except Exception as e:
            assert str(e) == "No items found for users"