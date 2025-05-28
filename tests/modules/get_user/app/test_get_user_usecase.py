import pytest

from src.modules.get_user.app.get_user_usecase import GetUserUsecase
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class TestGetUserUsecase:
    def test_get_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = GetUserUsecase(repo=repo)
        first_user = repo.users_list[0].user_id
        response = usecase(first_user)

        assert response == repo.users_list[0]


    def test_get_user_usecase_invalid_user_id(self):
        with pytest.raises(EntityError):
            repo = UserRepositoryMock()
            usecase = GetUserUsecase(repo=repo)
            reponse = usecase("invalid_user_id")

    def test_get_user_usecase_no_items_found(self):
        with pytest.raises(NoItemsFound):
            repo = UserRepositoryMock()
            usecase = GetUserUsecase(repo=repo)
            response = usecase("93bc6ada-c0d1-7054-26ab-e17414c48ae9")


