from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, 
                 user_id: str, 
                 confirm_user: bool, 
                 role: ROLE) -> User:
        
        if not User.validate_user_id(user_id):
            raise EntityError("user_id")

        if confirm_user and not User.validate_confirm_user(confirm_user):
            raise EntityError("new_confirm_user")
            
        if role and not User.validate_role(role):
            raise EntityError("new_role")
        
        updated_user = self.repo.update_user(user_id=user_id, new_role=role, new_confirm_user=confirm_user)
        if not updated_user:
            raise NoItemsFound("user")

        return updated_user

