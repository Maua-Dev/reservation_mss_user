from typing import Optional
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError

class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, user_id: str, confirm_user: bool, role: ROLE) -> User:
        
        if not user_id:
            raise EntityError("User ID must be provided")

        user = self.repo.get_user(user_id)
        if not user:
            raise EntityError("User not found")

 
        if not User.validate_confirm_user(confirm_user):
            raise EntityError("Invalid confirm_user value")
        
        if not User.validate_role(role):
            raise EntityError("Invalid role")

        user.confirm_user = confirm_user
        user.role = role

        updated_user = self.repo.update_user(user)

        return updated_user
