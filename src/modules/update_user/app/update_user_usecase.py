from typing import Optional

from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, ForbiddenAction


class UpdateUserUsecase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self, 
                 user_id: str,
                 new_confirm_user: Optional[bool],
                 new_role: Optional[str]) -> User:
        
        if not User.validate_user_id(user_id):
            raise EntityError("user_id")

        if new_confirm_user and not User.validate_confirm_user(new_confirm_user):
            raise EntityError("new_confirm_user")
            
        if new_role:

            try:
                new_role = ROLE(new_role)
            except:
                raise EntityError("new_role")

            if not User.validate_role(new_role):
                raise EntityError("new_role")

            # a student cant put himself as admin or professor
            user = self.repo.get_user(user_id=user_id)

            if user:
                if user.role == ROLE.STUDENT and new_role in [ROLE.ADMIN, ROLE.PROFESSOR]:
                    raise ForbiddenAction("student; trying to become admin or professor")
        
        updated_user = self.repo.update_user(user_id=user_id,
                                             new_role=new_role,
                                             new_confirm_user=new_confirm_user)
        if not updated_user:
            raise NoItemsFound("user")

        return updated_user

