from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.user import User


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
    def update_user(self, user_id: str, new_name: Optional[str] = None, new_email: Optional[str] = None,
                    new_ra: Optional[str] = None) -> Optional[User]:
        """
        Updates a user by id,
        takes new_name, new_email and new_ra as optional parameters
        """
        pass
