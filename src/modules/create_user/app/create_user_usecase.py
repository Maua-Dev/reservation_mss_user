from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.usecase_errors import DuplicatedItem


class CreateUserUseCase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self,
                 user_id: str,
                 name: str,
                 ra: str,
                 email: str,
                 role: ROLE,
                 confirm_user: bool) -> User:
        if self.repo.get_user(user_id=user_id) is not None:
            raise DuplicatedItem('user_id')

        user = User(user_id=user_id, name=name, ra=ra, email=email, role=role, confirm_user=confirm_user)

        return self.repo.create_user(user)
