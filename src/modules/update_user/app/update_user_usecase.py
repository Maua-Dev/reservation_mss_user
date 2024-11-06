from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str, confirm_user: bool, role: ROLE) -> User:
        
        if not User.validate_user_id:
            raise EntityError("user_id")

        user = self.repo.get_user(user_id)
        if not user:
            raise NoItemsFound ("user")
 
        if not User.validate_confirm_user(confirm_user):
            raise EntityError("confirm_user")
        
        if not User.validate_role(role):
            raise EntityError("role")

        user.confirm_user = confirm_user
        user.role = role

        updated_user = self.repo.update_user(user)

        return updated_user
