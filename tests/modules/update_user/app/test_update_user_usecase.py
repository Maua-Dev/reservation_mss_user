import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class MockUserRepository:
    def __init__(self): # Cria um usuário padrão para os testes
        self.user = User(
            name="Vini Berti",
            email="berti@gmail.com",
            user_id="93bc6ada-c0d1-8754-26ab-e17414c48ae7",
            ra=None,
            role=ROLE.PROFESSOR,
            confirm_user=False
        )

    def get_user(self, user_id: str) -> User:
        return self.user if user_id == self.user.user_id else None

    def update_user(self, user: User) -> User:
        self.user.confirm_user = user.confirm_user
        self.user.role = user.role
        return self.user

class TestUpdateUserUsecase:
    def test_update_user_success(self):
        repo = MockUserRepository()
        usecase = UpdateUserUsecase(repo=repo)

        updated_user = usecase(
            user_id="93bc6ada-c0d1-8754-26ab-e17414c48ae7", 
            confirm_user=True,
            role=ROLE.ADMIN
        )

        assert updated_user.confirm_user is True
        assert updated_user.role is ROLE.ADMIN

    def test_update_user_no_items_found(self):
            repo = UserRepositoryMock()
            usecase = UpdateUserUsecase(repo=repo)

            with pytest.raises(NoItemsFound):
                user = usecase(user_id="93bc6ada-c0d1-7054-66ab-e11111c48ae3",
                confirm_user= True,
                    role=ROLE.STUDENT)



    def test_update_user_invalid_confirm_user(self):
        repo = MockUserRepository()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError, match='Field confirm_user is not valid'):
            usecase(user_id="93bc6ada-c0d1-8754-26ab-e17414c48ae7", confirm_user=None, role=ROLE.STUDENT)
    
    
    def test_update_user_invalid_role(self):
        repo = MockUserRepository()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(EntityError, match='Field role is not valid'):
            usecase(user_id="93bc6ada-c0d1-8754-26ab-e17414c48ae7", confirm_user=True, role="INVALID_ROLE")



    
