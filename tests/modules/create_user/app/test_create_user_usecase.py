import pytest

from src.modules.create_user.app.create_user_usecase import CreateUserUsecase
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class TestCreateUserUsecase:

    def test_create_user_usecase_student(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        usecase(name="Jao do Bao", email="50.00847-4@maua.br", user_id="93bc6ada-c0d1-7054-26ab-e17414c48fe5")

        created_user = repo.users_list[-1]

        assert created_user.user_id == "93bc6ada-c0d1-7054-26ab-e17414c48fe5"
        assert created_user.email == "50.00847-4@maua.br"
        assert created_user.name == "Jao do Bao"
        assert created_user.ra == "50.00847-4"
        assert created_user.role == ROLE.STUDENT
        assert created_user.confirm_user is True

    def test_create_user_usecase_professor(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        usecase(name="Jao do Bao", email="jao.dobao@maua.br", user_id="93bc6ada-c0d1-7054-26ab-e17414f48fe5")

        created_user = repo.users_list[-1]

        assert created_user.user_id == "93bc6ada-c0d1-7054-26ab-e17414f48fe5"
        assert created_user.email == "jao.dobao@maua.br"
        assert created_user.name == "Jao do Bao"
        assert created_user.role == ROLE.PROFESSOR
        assert created_user.ra is None
        assert created_user.confirm_user is False

    def test_create_user_usecase_found_user(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(DuplicatedItem):

            usecase(name="Vini Berti", email="50.00847-4@maua.br", user_id="93bc6ada-c0d1-8754-26ab-e17414c48ae7")

    def test_create_user_usecase_entity_error(self):
        repo = UserRepositoryMock()
        usecase = CreateUserUsecase(repo)

        with pytest.raises(EntityError):

            usecase(name=1 , email="50.00847-4@maua.br", user_id="93bc6ada-c0d1-8754-26ab-e17414c48a77")
