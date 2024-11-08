from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class IUserRepository(ABC):

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        """
        Returns a user by a user_id (uuid)
        """
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        '''
        Returns all users
        '''
        pass

    @abstractmethod
    def create_user(self, new_user: User) -> User:
        '''
        Given a new user, creates it and returns it
        '''
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> Optional[User]:
        """
        Deletes user by id
        """
        pass

    @abstractmethod
    def update_user(self, user_id: str, new_confirm_user: Optional[bool] = False, new_role: Optional[ROLE] = ROLE.STUDENT) -> Optional[User]:
        """
        Updates a user by id,
        takes new_confirm_user and new_role as optional parameters
        """
        pass
